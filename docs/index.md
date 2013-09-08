# Droptype-Content

The `droptype-content` package is a Python wrapper for the Droptype Content API. The API provides for storage and query of content objects, supporting arbitrary properties.


## Reference

### `ContentObjects(api_token, api_root='marquee.by/content')`

The `ContentObjects` class is the main tool for interacting with the API. Each `ContentObjects` instance is instantiated with an API token that corresponds to a single user and application.

```python
>>> from content import ContentObjects
>>> content_objects = ContentObjects(CONTENT_API_TOKEN)
```

The actual objects are represented by various wrapper classes that correspond with their type: `Container`, `Text`, `Embed`, `Image`.

```python
>>> from content import Container, Text, Embed, Image
```

#### `ContentObjects::all()`

Retrieve a listing of objects. Equivalent to calling `filter()` without parameters.

#### `ContentObjects::create(type_class, attributes)`

Create a content object of the specified type, with the specified parameters.

```python
>>> story = content_objects.create(Container, {
    'role': 'story',
    'published_date': datetime.utcnow(),
})
```

#### `ContentObjects::filter(**parameters)`

Retrieve a listing of objects, filtered by parameters.

```python
>>> text_objects = content_objects.filter(type=Text)
>>> [o for o in text_objects]
[<content.models.Text object at 0x10f1630d0>, <content.models.Text object at 0x10f6da990>, ...]
```

#### `ContentObjects::fetch(content_id)`

Retrieve a single object by ID.

```python
>>> story = content_objects.fetch('container:0abaee14126d4dfca8dbcf03e462cd48')
```

#### `ContentObjects::save(*objects)`

Save the specified object(s).

```python
>>> story.title = 'There and Back Again'
>>> content_objects.save(story)
```


### `APIQuery`

The `filter` method returns an `APIQuery` object, an iterable which represents the query (not unlike a `QuerySet`). It is lazy, and only makes a request to the API when the data is needed. This allows the query to be additionally constrained, such as limiting, sorting, or additional parameters, before being executed.

```python
>>> content_objects.filter(role='story')
<content.api.APIQuery object at 0x10f6da990>
```

The parameters can use `__` notation for more complicated queries, as well as dot notation for accessing sub-properties.

```python
>>> content_objects.filter(title__regex_i='green eggs and ham')
>>> content_objects.filter({ 'layout.align': 'left' })
```

Note: once the query has been executed, additional constraints cannot be applied.

#### `APIQuery::limit(n)`

Limit the number of results to return. MUST be an integer from `1` to `100`, inclusive (100 is a limit enforced by the API).

```python
>>> stories = content_objects.filter(role='story').limit(10)
>>> len(stories)
10
```

#### `APIQuery::sort(sorting)`

Sort the results by the given property and direction. The sorting MUST be a string that is the property to sort by (in ascending order). To sort in descending order, prepend the string with a '-'.

```python
>>> stories = content_objects.filter(role='story').sort('-published_date')
```

#### `APIQuery::offset(n)`

Skip the first N results. Useful for paging.

```python
>>> stories = stories.offset(10)
```

#### `APIQuery::map(fn)`

Execute the results, calling the given function on each resulting content object and returning a list of the return values of that function. Useful for wrapping the objects in more specific models.

```python
>>> content_objects.filter(role='story').map(Story)
[<Story object at 0x10f1630d0>, <Story object at 0x10f6da990>, ...]
```

#### `APIQuery::mapOnExecute(fn)`

Similar to `map`, but doesn’t actually execute the results. This allows for additional composing of the query.

```python
>>> stories = content_objects.filter(role='story').mapOnExecute(Story)
```

Then in a template, each story will be a Story object instead of just a Container:

```jinja
{% for story in stories.limit(5).sort('-created_date') %}
    {{ story }}
{% endfor %}
```

#### `APIQuery::undo()`

Resets the query results, putting it into an unexecuted state so it can be additionally constrained and reexecuted.


### `instanceFromRaw(object_dict)`

Wrap the given raw attributes in a corresponding type class (`Container`, `Image`, `Embed`, or `Text`).

```python
>>> from content import instanceFromRaw
>>> instanceFromRaw(json_blob)
<content.models.Container object at 0x10f6da990>
```


### `Container`, `Text`, `Image`, `Embed`

The objects returned by the wrapper have some methods for working with the data returned by the API. The properties of the objects can be accessed using standard attribute access (dot notation).

#### `<class>::get(property, default=None)`

Get a specific property, or the default (avoids an `AttributeError` if the property does not exist).

#### `<class>::toDict()`

Return a `dict` representation of the object.

```python
>>> story.toDict()
{'modified_date': datetime.datetime(2013, 8, 29, 16, 54, 25, 982000, tzinfo=<UTC>), 'type': 'container', 'role': 'story', ... }'
```

#### `<class>::toJSON()`

Return a JSON `str` representation of the object.

```python
>>> story.toJSON()
'{"modified_date": "2013-08-29T16:54:25.982000Z", "type": "container", "role": "story", ... }'
```

#### `<class>::toJSONSafe()`

Return a `dict` representation of the object that is suitable for serialization to JSON. Same as `toDict`, but with `datetime` values converted to ISO-format strings.

```python
>>> story_dict = story.toJSONSafe()
>>> json.dumps(story_dict)
{"modified_date": "2013-08-29T16:54:25.982000Z", "type": "container", "role": "story", ... }
```

#### `<class>::update(attrs)`

Bulk set the specified properties.

```python
>>> story.update({
    'byline': 'Lois Lane',
    'subtitle': 'Tired of being mistaken as a bird and a plane, the man of steel speaks out',
})
```
