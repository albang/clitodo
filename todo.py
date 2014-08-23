#!/usr/bin/env python
from peewee import *
from datetime import datetime
database = SqliteDatabase(':tache:')  # Create a database instance.


class Tache(Model):
    description = CharField()
    date_creation = DateTimeField()
    date_debut = DateTimeField()
    date_fin = DateTimeField()
    is_done = BooleanField()


    def get_tache_undone(cls):
        taches = Tache.select().where(Tache.is_done == False)
        return(taches)

    def get_tache_done(cls):
        taches = Tache.select().where(Tache.is_done == True)
        return(taches)

    def ajouter_tache(cls, description, date):
        current_tache = Tache(
            description=description,
            date_creation=date,
            is_done=False
        )
        current_tache.save()

    def count_tache_undone(cls):
        return(Tache.select().where(Tache.is_done == False).count())

    def count_tache_done(cls):
        return(Tache.select().where(Tache.is_done == True).count())

    def change_status(self):
        if self.is_done is True:
            self.is_done = False
        else:
            self.is_done = True
            self.date_fin = datetime.now()
            totoletag=Tag(name="test")
            totoletag.ajouter()
            self.ajoute_tag(totoletag)
        self.save()

    def delete2(self):
        self.delete_instance()

    def stringmoica(self, isSelected=False):
        my_string = ""
        if isSelected is True:
            my_string = ">"
        else:
            my_string = " "
        if self.date_fin:
            my_string += str(self.date_fin) + " " + self.description
            my_string += " " + str(self.duree())
        else:
            my_string += str(self.date_creation) + " " + self.description
        return(my_string)

    def ajoute_tag(self, ptTag):
        TacheTag(tag=ptTag, tache=self).save()

    def get_tags(self):
        maListe = []
        for tag in (Tag.select().join(TacheTag).join(Tache).where(Tache.id == self.id)):
            maListe.append(Tag(name=tag.name))
        return (maListe)

    def duree(self):
        if self.date_fin:
            duree = self.date_fin - self.date_creation
            duree_annee = duree.days // 365
            duree_mois = duree.days % 365 // 31
            duree_semaine = duree.days // 7
            duree_jour = duree.days
            duree_heure = (int)(duree.total_seconds() % 86400/3600)
            duree_minute = (int)(duree.total_seconds() % (86400*3600)/60)
            duree_seconde = (int)(duree.total_seconds() % (86400*3600*60))
            duree_str = "("
            if duree_annee > 0:
                duree_str += str(duree_annee) + "ans "
                duree_str += str(duree_mois) + "mois"
            elif duree_mois > 0:
                duree_str += str(duree_mois) + "mois "
                duree_str += str(duree_semaine) + "sem"
            elif duree_semaine > 0:
                duree_str += str(duree_semaine) + "sem "
                duree_str += str(duree_jour) + "j"
            elif duree_jour > 0:
                duree_str += str(duree_jour) + "j "
                duree_str += str(duree_heure) + "h"
            elif duree_heure > 0:
                duree_str += str(duree_heure) + "h "
                duree_str += str(duree_minute) + "m"
            elif duree_minute > 0:
                duree_str += str(duree_minute) + "m "
                duree_str += str(duree_seconde) + "s"
            else:
                duree_str += str(duree_seconde) + "s"
            duree_str += ")"
            return(duree_str)

    def getAction(self):
        listAction = ["Archiver", "Tagguer"]
        return(listAction)

    def len(self):
        return(len(str(self)))

    def __str__(self):
        return(Tache.renderer.render(self))



    def init_renderer(self):
        renderList =[{
                            'description':
                            {
                                'id': 0,
                                'functions': [str.capitalize,str],
                                'show': True,
                            }
                            },
                            {
                            'id': {
                                'id': 0,
                                'functions': [str],
                                'show': False,
                            }},
                            {
                             'date_creation':
                            {
                                'id': 0,
                                'functions': [str],
                                'show': False,
                            }
                           }]
        Tache.renderer = Renderer(renderList)
    class Meta:
        database = database


#Tache.create_table()
class Tag(Model):
    name = CharField()
    
    def ajouter(self):
        #Verification si le tag existe
        try:
            monTag = Tag.get(name=self.name)
            self.id = monTag.id
        except Exception:
            self.save()

    def get_tags(cls):
        all_tags = Tag.select()
        return(all_tags)

    def get_nb_tache(self):
        return(Tag.select().join(TacheTag).where(Tag.id == self.id).count())

    def stringmoica(self):
        return(self.name+"("+str(self.get_nb_tache())+")")

    def __str__(self):
        return(Tag.renderer.render(self))

    def init_renderer(self):
        renderList =[{
                        'name':
                        {
                            'id': 0,
                            'functions': [str],
                            'show': True,
                        }
                        },
                        {
                        'id': {
                            'id': 0,
                            'functions': [str],
                            'show': False,
                        }},
                        {
                        'get_nb_tache':
                        {
                            'id': 0,
                            'functions': [Renderer().addParenthesis,str],
                            'show': True,
                        }
                       }]

        Tag.renderer = Renderer(renderList)

    def metal(self,titi):
        return(str(titi))


    class Meta:
        database = database
#Tag.create_table()


class TacheTag(Model):
    tache = ForeignKeyField(Tache)
    tag = ForeignKeyField(Tag)

    def ajouter(self):
        try:
            self.save()
        except Exception as  e:
            print(e)

    class Meta:
        database = database

#TacheTag.create_table()


class Renderer(object):
    """docstring for renderer"""
    def __init__(self, displayTable = {}):
        super(Renderer, self).__init__()
        self.displayTable = displayTable

    def render(self, renderMe):
        strView = ""
        for displayItem in self.displayTable:
            for attribut, settings in displayItem.items():
                if settings["show"]:
                    functionId = settings["id"]
                    renderFunction = settings["functions"][functionId]
                    if callable(renderMe.__getattribute__(attribut)):
                        strView += renderFunction(renderMe.__getattribute__(attribut)())
                    else:
                        strView += renderFunction(renderMe.__getattribute__(attribut))
        return(strView)

    def addParenthesis(self, item):
        return("("+str(item)+")")