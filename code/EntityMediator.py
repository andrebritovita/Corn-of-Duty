import pygame
from code.Const import WIN_WIDTH, C_YELLOW, C_RED, ENTITY_SCORE
from code.DeadPlayer import DeadPlayer
from code.Entity import Entity
from code.AnimatedEnemy import AnimatedEnemy
from code.AnimatedPlayer import AnimatedPlayer
from code.EntityFactory import EntityFactory
from code.PlayerShot import PlayerShot
from code.TextFeedback import TextFeedback
from code.Background import Background
from code.Item import Item


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if ent is None:
            return
        if isinstance(ent, AnimatedEnemy) and ent.rect.right <= 0:
            ent.health = 0
        if isinstance(ent, PlayerShot) and ent.rect.left >= WIN_WIDTH:
            ent.health = 0

    @staticmethod
    def __give_score(ent: Entity, entity_list: list[Entity]):
        for player in entity_list:
            if isinstance(player, AnimatedPlayer):
                if player.name == ent.last_dmg:
                    player.score += ent.score
                    player.kills += 1
                    feedback = TextFeedback(text=f'+{ent.score}', position=ent.rect.center)
                    entity_list.append(feedback)

    @staticmethod
    def __give_corn(player: AnimatedPlayer, item: Item, entity_list: list[Entity]):
        player.corn_count += 1
        player.corn_collected += 1
        player.score += ENTITY_SCORE["Corn"]
        if pygame.mixer.get_init():
            try:
                pickup_sound = pygame.mixer.Sound("./asset/pickup.mp3")
                pickup_sound.set_volume(7.0)
                pickup_sound.play()
            except pygame.error:
                print("[AVISO] Erro ao tocar pickup.mp3")

        feedback = TextFeedback(text="Milho +1", position=item.rect.center, color=C_YELLOW)
        entity_list.append(feedback)
        item.health = 0

    @staticmethod
    def __verify_collision_entity(ent1: Entity, ent2: Entity):
        if ent1 is None or ent2 is None:
            return None

        if isinstance(ent1, (TextFeedback, Background)) or isinstance(ent2, (TextFeedback, Background)):
            return None

        valid_interaction = False

        if isinstance(ent1, PlayerShot) and isinstance(ent2, AnimatedEnemy):
            valid_interaction = True
        elif isinstance(ent2, PlayerShot) and isinstance(ent1, AnimatedEnemy):
            valid_interaction = True
        elif isinstance(ent1, AnimatedPlayer) and isinstance(ent2, AnimatedEnemy):
            valid_interaction = True
        elif isinstance(ent2, AnimatedPlayer) and isinstance(ent1, AnimatedEnemy):
            valid_interaction = True

        if valid_interaction and ent1.rect.colliderect(ent2.rect):
            if isinstance(ent1, PlayerShot) and isinstance(ent2, AnimatedEnemy):
                feedback = TextFeedback(text=f'-{ent1.damage}', position=ent2.rect.center, color=C_RED)
                ent2.take_damage(ent1.damage)
                ent1.health = 0
                ent2.last_dmg = ent1.player_name
                return feedback

            elif isinstance(ent2, PlayerShot) and isinstance(ent1, AnimatedEnemy):
                feedback = TextFeedback(text=f'-{ent2.damage}', position=ent1.rect.center, color=C_RED)
                ent1.take_damage(ent2.damage)
                ent2.health = 0
                ent1.last_dmg = ent2.player_name
                return feedback

            player, enemy = None, None
            if isinstance(ent1, AnimatedPlayer) and isinstance(ent2, AnimatedEnemy):
                player, enemy = ent1, ent2
            elif isinstance(ent2, AnimatedPlayer) and isinstance(ent1, AnimatedEnemy):
                player, enemy = ent2, ent1

            if player and enemy:
                if player.attack_timer > 0:
                    feedback = TextFeedback(text=f'-{player.damage}', position=enemy.rect.center, color=C_RED)
                    enemy.take_damage(player.damage)
                    enemy.last_dmg = player.name
                    return feedback
                elif player.invincibility_timer == 0:
                    player.take_damage(enemy.damage)
                    feedback = TextFeedback(text=f'-{enemy.damage}', position=player.rect.center, color=C_RED)
                    return feedback

        return None

    @staticmethod
    def verify_pickup_item(entity_list: list[Entity]):
        players = [p for p in entity_list if isinstance(p, AnimatedPlayer)]
        items = [i for i in entity_list if isinstance(i, Item)]

        for player in players:
            for item in items:
                if player.rect.colliderect(item.rect):
                    EntityMediator.__give_corn(player, item, entity_list)

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        all_collisions = []

        EntityMediator.verify_pickup_item(entity_list)

        for i in range(len(entity_list)):
            ent1 = entity_list[i]
            EntityMediator.__verify_collision_window(ent1)
            for j in range(i + 1, len(entity_list)):
                ent2 = entity_list[j]
                feedback = EntityMediator.__verify_collision_entity(ent1, ent2)
                if feedback:
                    all_collisions.append(feedback)
        return all_collisions

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        entities_to_remove = []
        explosion_sound = None
        if pygame.mixer.get_init():
            try:
                explosion_sound = pygame.mixer.Sound("./asset/explosion.wav")
            except pygame.error:
                print("[AVISO] Erro ao tocar explosion.wav")

        for ent in entity_list:
            if not ent or not hasattr(ent, "health"):
                continue
            if isinstance(ent, (Background, TextFeedback)):
                continue

            if ent.health <= 0:
                if isinstance(ent, AnimatedEnemy):
                    if explosion_sound:
                        explosion_sound.play()
                    EntityMediator.__give_score(ent, entity_list)

                    dead_entity = EntityFactory.get_entity(ent.original_name.replace("Enemy", "EnemyDead"))
                    if dead_entity:
                        dead_entity.rect.center = ent.rect.center
                        entity_list.append(dead_entity)

                elif isinstance(ent, AnimatedPlayer):
                    if not any(isinstance(e, DeadPlayer) and e.name == f'{e.name}Die' for e in entity_list):
                        entity_list.append(DeadPlayer(ent.rect.center, player_name=ent.name))

                entities_to_remove.append(ent)

        for ent_to_remove in entities_to_remove:
            if ent_to_remove in entity_list:
                entity_list.remove(ent_to_remove)

    @staticmethod
    def get_players_from_list(entity_list: list[Entity]):
        return [ent for ent in entity_list if isinstance(ent, AnimatedPlayer)]
