from peewee import *
import time

db = SqliteDatabase('bot.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    UID = BigIntegerField(unique=True)
    SUB = BigIntegerField(default=0)
    UTA = BooleanField(default=False)

    @classmethod
    def get_users(cls):
        return cls.select()

    @classmethod
    def get_user(cls, UID):
        return cls.get(cls.UID == UID)

    @classmethod
    def used_trial_access(cls, UID):
        return cls.get(cls.UID == UID).UTA

    @classmethod
    def have_sub(cls, UID):
        return cls.get(cls.UID == UID).SUB > time.time()

    @classmethod
    def sub_until(cls, UID):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cls.get(cls.UID == UID).SUB))

    @classmethod
    def user_exists(cls, UID):
        query = cls().select().where(cls.UID == UID)
        return query.exists()

    @classmethod
    def create_user(cls, UID):
        user, created = cls.get_or_create(UID=UID)

    @classmethod
    def give_sub(cls, UID, DAY):
        base = cls.get(cls.UID == UID)
        base.SUB = time.time() + (86400 * DAY)
        base.save()

    @classmethod
    def take_sub(cls, UID):
        base = cls.get(cls.UID == UID)
        base.SUB = 0
        base.save()

    @classmethod
    def give_trial(cls, UID):
        base = cls.get(cls.UID == UID)
        base.UTA = True
        base.SUB = time.time() + (60 * 10)
        base.save()

    @classmethod
    def get_users_count(cls):
        return len(cls.select())

    @classmethod
    def get_subs_count(cls):
        return len(cls.select().where(cls.SUB > time.time()))

class Bombs(BaseModel):
    UID = BigIntegerField()
    BID = TextField(unique=True)
    NUM = TextField(default='')
    ITR = IntegerField(default=0)
    GITR = IntegerField(default=0)

    @classmethod
    def create_bomb(cls, UID, BID, NUM, ITR):
        bomb, created = cls.get_or_create(UID=UID, BID=BID, NUM=NUM, ITR=ITR)

    @classmethod
    def get_bomb(cls, BID):
        return cls.get(cls.BID == BID)

    @classmethod
    def get_bombs(cls):
        return cls.select()

    @classmethod
    def get_bombs_count(cls):
        return len(cls.select())

    @classmethod
    def bomb_alive(cls, BID):
        query = cls().select().where(cls.BID == BID)
        return query.exists()

    @classmethod
    def goed_iteration(cls, BID):
        base = cls.get(cls.BID == BID)
        base.GITR += 1
        base.save()

    @classmethod
    def get_bombs_count_by_id(cls, UID):
        return len(cls.select().where(cls.UID == UID))

    @classmethod
    def get_bombs_by_id(cls, UID):
        return cls.select().where(cls.UID == UID)

class Whitelist(BaseModel):
    UID = BigIntegerField()
    NUM = TextField(default='')

    @classmethod
    def create_whitelist(cls, UID, NUM):
        bomb, created = cls.get_or_create(UID=UID, NUM=NUM)

    @classmethod
    def get_whitelist(cls, NUM):
        return cls.get(cls.NUM == NUM)

    @classmethod
    def get_whitelists(cls):
        return cls.select()

    @classmethod
    def get_whitelist_count(cls):
        return len(cls.select())

    @classmethod
    def in_whitelist(cls, NUM):
        query = cls().select().where(cls.NUM == NUM)
        return query.exists()

    @classmethod
    def get_whitelist_count_by_id(cls, UID):
        return len(cls.select().where(cls.UID == UID))

    @classmethod
    def get_whitelist_by_id(cls, UID):
        return cls.select().where(cls.UID == UID)

db.create_tables([Users, Bombs, Whitelist])