# Putting Python on the map

---?image=presentation/images/intro-title-card.png&size=100%

---?image=presentation/images/hey-why-not.png&size=60%

---?image=presentation/images/scales.jpg&size=80%

---
### Foreign key
- Reference that uniquely identifies a model
- Implemented at database level
- Firm guarantees of referential integrity
- Automatically indexed for performance
- Effortless querying forward and backwards

+++?image=presentation/images/referential_integrity_1.png&size=80%
## Referential Integrity

+++?image=presentation/images/cascade.png&size=80%
## Cascade

+++?image=presentation/images/protect.png&size=80%
## Protect

+++?image=presentation/images/set_null.png&size=80%
## Set null

---
### Generic foreign key
- Reference that uniquely identifies a model
- ~~Implemented at database level~~
- ~~Firm guarantees of referential integrity~~
- ~~Automatically indexed for performance~~
- ~~Effortless querying forward and backwards~~

---?image=presentation/images/scarcely.png

---

### Generic foreign keys have this one weird trick
- ForeignKey can refer to one type of model
- GFKs can refer to any model in your application

---
### Let's keep track of changes to our models
```py
class Event(models.Model):
    changes = JSONField()
    occurred_at = models.DateTimeField(auto_now_add=True)

    object_id = models.BigIntegerField()
    content_type = models.ForeignKey(ContentType)
    subject = GenericForeignKey('content_type', 'object_id')
```
@[1-3](We want to serialize the changes, and when they occurred)
@[5](We will store the ID of the model that changed)
@[6](We will store the type of the model that changed)
@[5-7](Wrap content_type and object_id as a GFK)

---
### What is GenericForeignKey doing?
```py
class GenericForeignKey(object):
    def contribute_to_class(self, cls, name, **kwargs):
        cls._meta.add_field(self, private=True)
        setattr(cls, name, self)

    def __get__(self, instance):
        return instance.content_type.get_object_for_this_type(
            instance.object_id
        )
```
@[2-4](Add self as a field on the model class)
@[6-9](Work as a descriptor using content type and object ID to return referenced model)

---
### Record a change to a model
```py
class Cleaner(models.Model):
    name = models.CharField(max_length=128)

def set_cleaner_name(cleaner, name):
    cleaner.name = name
    cleaner.save()
    Event.objects.create(
        subject=cleaner,
        changes={'name': name}
    )
```
@[8]

---
### Record a change to a different type of model
```py
class Job(models.Model):
    cleaner = models.ForeignKey(Cleaner)
    started_at = models.DateTimeField()

def assign_job(job, cleaner):
    job.cleaner = cleaner
    job.save()
    Event.objects.create(
        subject=job,
        changes={'cleaner': cleaner.id}
    )
```
@[9]

---
### Retrieval
```py
>>> first_event = Event.objects.order_by('occurred_at').first()
>>> first_event.subject

<Job: "Cleaning at Pam's">

>>> last_event = Event.objects.order_by('occurred_at').last()
>>> last_event.subject

<Cleaner: "Alex">
```

---
### Querying
```
>>> cleaner = Cleaner.objects.get(name='Alex')
>>> Event.objects.filter(subject=cleaner)

---------------------------------------------------------------------------
FieldError                                Traceback (most recent call last)
...
FieldError: Field 'subject' does not generate an automatic reverse relation...


>>> content_type = ContentType.objects.get_for_model(Cleaner)
>>> Spam.objects.filter(content_type=content_type, object_id=cleaner.id)]

<QuerySet [<Event: 'Name changed to Alex'>]>
```
@[10-11](We have to query explicitly on the content type and ID fields)

---
### GenericRelation

```py
class Cleaner(models.Model):
    name = models.CharField(max_length=128)
    events = GenericRelation(Event)

>>> cleaner.events.filter(occurred_at__gte=date.today())

<QuerySet [<Event: 'Name changed to Alex'>]>
```
@[3](We know cleaners will be the subjects of events, so we can add the 'reverse' relationship)
@[5-7](We can now query similarly to the reverse relationship of a traditional foreign key)

---
### GenericRelation with related query name
```py
class Cleaner(models.Model):
    name = models.CharField(max_length=128)
    events = GenericRelation(related_query_name='cleaners')

>>> Event.objects.filter(cleaners__name='Frederick')
<QuerySet [<Event: 'Name changed to Frederick'>]>
```
@[3]
@[5-7]

```sql
SELECT *
FROM "events_event"
INNER JOIN "cleaners_cleaner" ON (
    "events_event"."instance_id" = "cleaners_cleaner"."id"
    AND ("events_event"."content_type_id" = 41)
)
WHERE "cleaners_cleaner"."name" = 'gareth'
```
@[8-13]

---
### GenericRelation also enables aggregation
```py
>>> Cleaner.objects.aggregate(Min('events__occurred_at'))

{
    'events__created__min': (
        datetime.datetime(2015, 2, 26, 20, 35, 18, 771908, tzinfo=<UTC>)
    )
}

>>> cleaners = Cleaner.objects.annotate(Count('events'))
>>> cleaner = cleaners.get(name='Frederick')
>>> cleaner.events__count

2
```

---
## Ability to make polymorphic links between models, with a nice Django-style API

---
## Generic foreign keys considered harmful?

Core developers are warning us off

Luke Plant: <a href="https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/" target="_blank">Avoid Generic Foreign keys</a>.

Marc Tamlyn: <a href="https://www.youtube.com/watch?v=aDt4gu99_bE" target="_blank">Weird and wonderful things to do with the ORM</a>.

---
## Referential integrity

---
## Lack of `on_delete` support

---
## Model changes can hurt your data

Let's change `Cleaner` to `HomeCleaner`

```sh
$ ./manage.py makemigrations
$ ./manage.py migrate
```

```py
>>> Event.objects.first().subject

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
/srv/housekeep/housekeep/fixes/shortcuts/__init__.pyc in <module>()

AttributeError: 'NoneType' object has no attribute '_base_manager'
```
---
## It's just too loosey goosey

---
# My def
---
## Applications: adding common metadata across models
- Revisions
- Tags
- Common properties, such as telephone numbers

---
### Applications: adding additional content related to any model
- Comments
- Tickets
- Ratings

---
### Applications: containing many different things
- Tumble log entry
  - Can contain a link, a video, an image etc

---
### Applications: portable third party apps
- You run an email service, and you want to provide a Django app
- Create your own model to record a sent email
- Add GFKs for sent_to and sent_by
  - Any model in the user's app can send to any other model

---
Used properly, can enable:
- Looser coupling
- Extensability
- Openness about the future

---
## So there are these great applications. Can we overcome the bad bits?
