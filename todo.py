#!/usr/bin/env python
from peewee import *
from datetime import datetime
import logging
database = SqliteDatabase(':tache:')  # Create a database instance.

logging.basicConfig(filename='example.log', level=logging.DEBUG)

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

    def get_tache_to_show(cls):
        if len(Tag.hidedTag) : 
            #taches = Tache.select().join(TacheTag).join(Tag).where(Tache.id == self.id)
            taches = Tache.select(Tache).distinct().join(TacheTag).join(Tag).where(Tag.id != Tag.hidedTag[0].id)
        else:
            taches = Tache.select(Tache)

        for tache in taches:
            tache.get_tags() 
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
            self.ajoute_tag(ptTag=Tag().ajouter(name="undone"))
            self.deleteTag("done")
        else:
            self.is_done = True
            self.date_fin = datetime.now()
            self.ajoute_tag(ptTag=Tag().ajouter(name="done"))
            self.deleteTag("undone")
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
        try:
            TacheTag.create(tag=ptTag, tache=self)
        except Exception as e:
            logging.error(e)

    def deleteTag(self,tagName="caca"):
        try:
            delTag = TacheTag.get(tag=Tag().ajouter(name=tagName),tache=self)
            delTag.delete_instance()
        except Exception as e:
            logging.warning(e)

    def tagCaca(self):
        logging.info("[pb1]"+self.description+" Tag caca ")
        self.ajoute_tag(ptTag=Tag().ajouter(name="caca"))
        pass

    def get_tags(self):
        maListe = []
        for tag in (Tag.select().join(TacheTag).join(Tache).where(Tache.id == self.id)):
            maListe.append(Tag(name=tag.name))
        self.tags = maListe
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
                duree_str += str(duree_sloggeemaine) + "sem"
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
        listAction = [{'Archiver': {
                      'action': self.archiveMe,
                      'show': True,
                      }},
                      {'Tagguer': {
                       'action': self.tagCaca,
                       'show': True,
                       }},
                      {'Delete Tag': {
                       'action': self.deleteTag,
                       'show': True,
                       }
                       }]
        if self.is_done:
            listAction.append({'undone this task': {
                              'action': self.change_status,
                              'show': True,
                              }})
        else:
            listAction.append({'done this task': {
                              'action': self.change_status,
                              'show': True,
                              }})
        listAction.append({'Cancel': {
                              'action': self.cancel,
                              'show': True,
                              }})
        return(listAction)

    def cancel(self):
        pass

    def archiveMe(self):
        pass

    def len(self):
        return(len(str(self)))

    def cache_nb_tag(fonctionADecorer,self):
        def wrapper(self):
            hasChanged = Tag.hideNbTaches()
            monStr = fonctionADecorer(self)
            if hasChanged:
                Tag.showNbTaches
            return(monStr)

    def __str__(self):
        hasChanged = Tag.hideNbTaches()
        monStr = Tache.renderer.render(self)
        if hasChanged:
            Tag.showNbTaches
        return(monStr)



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
                           },
                           {
                             'tags':
                            {
                                'id': 0,
                                'functions': [Renderer().concatTag,str],
                                'show': True,
                            }
                           }]
        Tache.renderer = Renderer(renderList)
    class Meta:
        database = database


#Tache.create_table()
class Tag(Model):
    name = CharField()
    hidedTag = []

    def ajouter(self, name):
        #Verification si le tag existe
        try:
            monTag = Tag.get(name=name)
            self.id = monTag.id
        except Exception:
            monTag = Tag(name=name)
            monTag.save()
        return(monTag)

    def get_tags(cls):
        all_tags = Tag.select()
        return(all_tags)

    def get_nb_tache(self):
        return(Tag.select().join(TacheTag).where(Tag.id == self.id).count())

    def stringmoica(self):
        return(self.name+"("+str(self.get_nb_tache())+")")

    def getAction(self):
        listAction = [{'Archiver': {
                      'action': self.archiveMe,
                      'show': True,
                      }},
                      {'Delete Tag': {
                       'action': self.deleteTag,
                       'show': True,
                       }
                       }]
        if self in Tag.hidedTag:
            listAction.append({'show': {
                              'action': self.change_status,
                              'show': True,
                              }})
        else:
            listAction.append({'hide': {
                              'action': self.change_status,
                              'show': True,
                              }})
        listAction.append({'Cancel': {
                              'action': self.cancel,
                              'show': True,
                              }})
        return(listAction)

    def cancel(self):
        pass

    def archiveMe(self):
        pass

    def change_status(self):
        if self in Tag.hidedTag:
            Tag.hidedTag.remove(self)
            logging.info("[change_status][TAG] Show "+self.name)
        else:
            Tag.hidedTag.append(self)
            logging.info("[change_status][TAG] Hide "+self.name)

        pass

    def deleteTag(self):
        
        self.delete_instance(True)

    def __str__(self):
        return(Tag.renderer.render(self))

    def init_renderer(self):
        renderList = [{
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
    @classmethod
    def hideNbTaches(cls):
        hasChanged = cls.renderer.hide_attribut("get_nb_tache")
        return(hasChanged)
    @classmethod
    def showNbTaches(cls):
        hasChanged = cls.renderer.show_attribut("get_nb_tache")
        return(hasChanged)

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
        primary_key = CompositeKey('tache', 'tag')


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
        return("(" + str(item) + ")")

    def concatTag(self, tags):
        tagStr = ""
        for tag in tags:
            tagStr += " " + str(tag)
        return(tagStr)

    def hide_attribut(self, attributHide):
        hasChanged = False
        for displayItem in self.displayTable:
            for attribut, settings in displayItem.items():
                if attribut ==  attributHide and settings["show"]:
                    settings["show"] = False
                    hasChanged = True
        return(hasChanged)

    def show_attribut(self, attributHide):
        hasChanged = False
        for displayItem in self.displayTable:
            for attribut, settings in displayItem.items():
                if attribut == attributHide and settings["show"] is False:
                    settings["show"] = True
                    hasChanged = True
        retun(True)