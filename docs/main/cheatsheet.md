# Text-Fabric API

## Advanced API

### Initialisation, configuration, meta data, and linking

```A = use('corpus', hoist=globals())```
:   start up
:   `tf.app.use`

```A.reuse()```
:   reload config data
:   `tf.applib.app.App.reuse`

```A.showContext(...)```
:   show app settings
:   `tf.applib.settings.showContext`

```A.header()```
:   show colofon
:   `tf.applib.links.header`

```A.showProvenance(...)```
:   show provenance of code and data
:   `tf.applib.links.showProvenance`

```A.webLink(n, ...)```
:   hyperlink to node n on the web
:   `tf.applib.links.webLink`


### Displaying

```method(option1=value1, option2=value2, ...)```
:   Many of the following methods accept these options as keyword arguments: 
:   `tf.applib.displaysettings`

```A.displaySetup(...)```
:   set up display options
:   `tf.applib.display.displaySetup`

```A.displayReset(...)```
:   resetdisplay options
:   `tf.applib.display.displayReset`

```A.table(results, ...)```
:   plain rendering of tuple of tuples of node
:   `tf.applib.display.table`

```A.plainTuple(tup, ith, ...)```
:   plain rendering of tuple of node
:   `tf.applib.display.plainTuple`

```A.plain(node, ...)```
:   plain rendering of node
:   `tf.applib.display.plain`

```A.show(results, ...)```
:   pretty rendering of tuple of tuples of node
:   `tf.applib.display.show`

```A.prettyTuple(tup, ith, ...)```
:   pretty rendering of tuple of node
:   `tf.applib.display.prettyTuple`

```A.pretty(node, ...)```
:   pretty rendering of node
:   `tf.applib.display.pretty`


### Search (high level)

```A.search(...)```
:   search, collect and deliver results, report number of results
:   `tf.applib.search.search`


### Sections and Structure

```A.nodeFromSectionStr(...)```
:   lookup node for sectionheading
:   `tf.applib.sections.nodeFromSectionStr`

```A.sectionStrFromNode(...)```
:   lookup section heading for node
:   `tf.applib.sections.sectionStrFromNode`

```A.structureStrFromNode(...)```
:   lookup structure heading for node
:   `tf.applib.sections.structureStrFromNode`


## Core API

### Dataset

#### Loading

```TF = Fabric(locations=directories, modules=subdirectories, silent=False)```
:   Initialize API on dataset from explicit directories.
    Use `tf.app.use` instead wherever you can.
:   `tf.fabric.Fabric`

```TF.explore(show=True)```
:   Get features by category, loaded or unloaded
:   `tf.fabric.Fabric.explore`

```TF.loadAll(silent=None)```
:   Load all loadable features. 
:   `tf.fabric.Fabric.loadAll`

```TF.load(features, add=False)```
:   Load a bunch of features from scratch or additionally. 
:   `tf.fabric.Fabric.load`

```ensureLoaded(features)```
:   Make sure that features are loaded.
:   `tf.core.api.Api.ensureLoaded`

```makeAvailableIn(globals())```
:   Make the members of the core API available in the global scope
:   `tf.core.api.Api.makeAvailableIn`

```ignored```
:   Which features have been overridden.
:   `tf.core.api.Api.ignored`

```loadLog()```
:   Log of the feature loading process
:   `tf.core.api.Api.loadLog`

#### Saving

```TF.save(nodeFeatures={}, edgeFeatures={}, metaData={},,...)```
:   Save a bunch of newly generated features to disk.
:   `tf.fabric.Fabric.save`

### Nodes

Read about the canonical ordering here: `tf.core.api`.

```N()```
:   generator of all nodes in canonical ordering
:   `tf.core.api.Api.N`

```sortNodes(nodes)```
:   sorts `nodes` in the canonical ordering
:   `tf.core.api.Api.sortNodes`

```otypeRank[nodeType]```
:   ranking position of `nodeType`
:   `tf.core.api.Api.otypeRank`

```sortKey(node)```
:   defines the canonical ordering on nodes
:   `tf.core.api.Api.sortKey`

```sortKeyTuple(tup)```
:   extends the canonical ordering on nodes to tuples of nodes
:   `tf.core.api.Api.sortKeyTuple`

```sortKeyChunk(node)```
:   defines the canonical ordering on node chunks
:   `tf.core.api.Api.sortKeyChunk`

### Features

#### Node features

```Fall()```
:   all loaded feature names (node features only)
:   `tf.core.api.Api.Fall`

```F.fff.v(node)```
:   get value of node feature `fff`
:   `tf.core.api.NodeFeature.v`

```F.fff.s(value)```
:   get nodes where feature `fff` has `value`
:   `tf.core.api.NodeFeature.s`

```F.fff.freqList(...)```
:   frequency list of values of `fff`
:   `tf.core.api.NodeFeature.freqList`

```F.fff.items(...)```
:   generator of all entries of `fff` as mapping from nodes to values
:   `tf.core.api.NodeFeature.items`

```F.fff.meta```
:   meta data of feature `fff`
:   `tf.core.api.NodeFeature.meta`

```Fs('fff')```
:   identical to `F.ffff`, usable if name of feature is variable
:   `tf.core.api.Api.Fs`

#### Special feature `otype`

Maps nodes to their types.

```F.otype.v(node)```
:   get type of `node`
:   `tf.core.api.OtypeFeature.v`

```F.otype.s(nodeType)```
:   get all nodes of type `nodeType`
:   `tf.core.api.OtypeFeature.s`

```F.otype.sInterval(nodeType)```
:   gives start and ending nodes of `nodeType`
:   `tf.core.api.OtypeFeature.sInterval`

```F.otype.items(...)```
:   generator of all (node, type) pairs.
:   `tf.core.api.OtypeFeature.items`

```F.otype.meta```
:   meta data of feature `otype`
:   `tf.core.api.OtypeFeature.meta`

```F.otype.maxSlot```
:   the last slot node
:   `tf.core.api.OtypeFeature.maxSlot`

```F.otype.maxNode```
:   the last node
:   `tf.core.api.OtypeFeature.maxNode`

```F.otype.slotType```
:   the slot type
:   `tf.core.api.OtypeFeature.slotType`

```F.otype.all```
:   sorted list of all node types
:   `tf.core.api.OtypeFeature.all`

#### Edge features

```Eall()```
:   all loaded feature names (edge features only)
:   `tf.core.api.Api.Eall`

```E.fff.f(node)```
:   get value of feature `fff` for edges *from* node
:   `tf.core.api.EdgeFeature.f`

```E.fff.t(node)```
:   get value of feature `fff` for edges *to* node
:   `tf.core.api.EdgeFeature.t`

```E.fff.freqList(...)```
:   frequency list of values of `fff
:   `tf.core.api.EdgeFeature.freqList`

```E.fff.items(...)```
:   generator of all entries of `fff` as mapping from edges to values
:   `tf.core.api.EdgeFeature.items`

```E.fff.b(node)```
:   get value of feature `fff` for edges *from* and *to* node
:   `tf.core.api.EdgeFeature.b`

```E.fff.meta```
:   all meta data of feature `fff`
:   `tf.core.api.EdgeFeature.meta`

```Es('fff')```
:   identical to `E.fff`, usable if name of feature is variable
:   `tf.core.api.Api.Es`

#### Special feature `oslots`

Maps nodes to the set of slots they occupy.

```E.oslots.items(...)```
:   generator of all entries of `oslots` as mapping from nodes to sets of slots
:   `tf.core.api.OslotsFeature.items`

```E.oslots.s(node)```
:   set of slots linked to `node`
:   `tf.core.api.OslotsFeature.s`

```E.oslots.meta```
:   all meta data of feature `oslots`
:   `tf.core.api.OslotsFeature.meta`

### Locality

```L.i(node, otype=...)```
:   go to intersecting nodes
:   `tf.core.locality.Locality.i`

```L.u(node, otype=...)```
:   go one level up
:   `tf.core.locality.Locality.u`

```L.d(node, otype=...)```
:   go one level down
:   `tf.core.locality.Locality.d`

```L.p(node, otype=...)```
:   go to adjacent previous nodes
:   `tf.core.locality.Locality.p`

```L.n(node, otype=...)```
:   go to adjacent next nodes
:   `tf.core.locality.Locality.n`

### Text

```T.text(node, fmt=..., ...)```
:   give formatted text associated with node
:   `tf.core.text.Text.text`

### Sections

Rigid 1 or 2 or 3 sectioning system

```T.sectionTuple(node)```
:   give tuple of section nodes that contain node
:   `tf.core.text.Text.sectionTuple`

```T.sectionFromNode(node)```
:   give section heading of node
:   `tf.core.text.Text.sectionFromNode`

```T.nodeFromSection(section)```
:   give node for section heading
:   `tf.core.text.Text.nodeFromSection`

### Structure

Flexible multilevel sectioning system

```T.headingFromNode(node)```
:   give structure heading of node
:   `tf.core.text.Text.headingFromNode`

```T.nodeFromHeading(heading)```
:   give node for structure heading
:   `tf.core.text.Text.nodeFromHeading`

```T.structureInfo()```
:   give summary of dataset structure
:   `tf.core.text.Text.structureInfo`

```T.structure(node)```
:   give structure of `node` and all in it.
:   `tf.core.text.Text.structure`

```T.structurePretty(node)```
:   pretty print structure of `node` and all in it.
:   `tf.core.text.Text.structurePretty`

```T.top()```
:   give all top-level structural nodes in the dataset
:   `tf.core.text.Text.top`

```T.up(node)```
:   gives parent of structural node
:   `tf.core.text.Text.up`

```T.down(node)```
:   gives children of structural node
:   `tf.core.text.Text.down`

### Search (low level)

#### Preparation

```S.search(query, limit=None)```
:   Query the TF dataset with a template
:   `tf.search.search.Search.search`

```S.study(query, ...)```
:   Study the query in order to set up a plan
:   `tf.search.search.Search.study`

```S.showPlan(details=False)```
:   Show the search plan resulting from the last study.
:   `tf.search.search.Search.showPlan`

```S.relationsLegend()```
:   Catalog of all relational devices in search templates
:   `tf.search.search.Search.relationsLegend`

#### Fetching results

```S.count(progress=None, limit=None)```
:   Count the results, up to a limit
:   `tf.search.search.Search.count`

```S.fetch(limit=None, ...)```
:   Fetches the results, up to a limit
:   `tf.search.search.Search.fetch`

```S.glean(tup)```
:   Renders a single result into something human readable.
:   `tf.search.search.Search.glean`

#### Implementation

```S.tweakPerformance(...)```
:   Set certain parameters that influence the performance of search.
:   `tf.search.search.Search.tweakPerformance`

### Logging

```TF.version```
:   version number of the Text-Fabric package.
:   `tf.fabric.Fabric.version`

```TF.banner```
:   banner of the Text-Fabric program.
:   `tf.fabric.Fabric.banner`

```isSilent()```
:   report the verbosity of Text-Fabric
:   `tf.core.timestamp.Timestamp.isSilent`

```silentOn(deep=False)```
:   make TF silent from now on.
:   `tf.core.timestamp.Timestamp.silentOn`

```silentOff()```
:   make TF talkative from now on.
:   `tf.core.timestamp.Timestamp.silentOff`

```setSilent(silent)```
:   set the verbosity of Text-Fabric.
:   `tf.core.timestamp.Timestamp.setSilent`

```indent(level=None, reset=False)```
:   Sets up indentation and timing of following messages
:   `tf.core.timestamp.Timestamp.indent`

```info(msg, tm=True, nl=True, ...)```
:   informational message
:   `tf.core.timestamp.Timestamp.info`

```warning(msg, tm=True, nl=True, ...)```
:   warning message
:   `tf.core.timestamp.Timestamp.warning`

```error(msg, tm=True, nl=True, ...)```
:   error message
:   `tf.core.timestamp.Timestamp.error`

### Computed data components.

Access to precomputed data: `tf.core.api.Computeds`.

All components have just one useful attribute: `.data`.

```Call()```
:   all precomputed data component names
:   `tf.core.api.Api.Call`

```Cs('ccc')```
:   identical to `C.ccc`, usable if name of component is variable
:   `tf.core.api.Api.Cs`

```C.levels.data```
:   various statistics on node types
:   `tf.core.prepare.levels`

```C.order.data```
:   the canonical order of the nodes (`tf.core.api`)
:   `tf.core.prepare.order`

```C.rank.data```
:   the rank of the nodes in the canonical order (`tf.core.api`)
:   `tf.core.prepare.rank`

```C.levUp.data```
:   feeds the `tf.core.locality.Locality.u` function
:   `tf.core.prepare.levUp`

```C.levDown.data```
:   feeds the `tf.core.locality.Locality.d` function
:   `tf.core.prepare.levDown`

```C.boundary.data```
:   feeds the `tf.core.locality.Locality.p` and `tf.core.locality.Locality.n`
    functions
:   `tf.core.prepare.boundary`

```C.sections.data```
:   feeds the section part of `tf.core.text`
:   `tf.core.prepare.sections`

```C.structure.data```
:   feeds the structure part of `tf.core.text`
:   `tf.core.prepare.structure`

### House keeping

```TF.clearCache()```
:   clears the cache of compiled TF data
:   `tf.fabric.Fabric.clearCache`

```python
from tf.clean import clean
```

```clean()```
:   clears the cache of compiled TF data
:   `tf.clean`

## TF Dataset Manipulation

```python
from tf.compose import combine, modify
```

```combine((source1, source2, ...), target)```
:   Combines several TF datasets into one new TF dataset
:   `tf.compose.combine`

```modify(source, target, ...)```
:   Modifies a TF datasets into one new TF dataset
:   `tf.compose.modify`

## Data Interchange

### Custom node sets for search

```python
from tf.lib import readSets
from tf.lib import writeSets
```

```readSets(sourceFile)```
:   reads a named sets from file
:   `tf.lib.readSets`

```writeSets(sets, destFile)```
:   writes a named sets to file
:   `tf.lib.writeSets`

### Export to Excel

```A.export(results, ...)```
:   export formatted data
:   `tf.applib.display.export`

### MQL interchange

```TF.exportMQL()```
:   export loaded dataset to MQL
: `tf.fabric.Fabric.exportMQL`

```TF.importMQL()```
:   convert MQL file to TF dataset
:   `tf.fabric.Fabric.importMQL`

### Walker conversion

```python
from tf.convert.walker import CV
```

```cv = CV(TF)```
:   convert structured data to TF dataset
:   `tf.convert.walker`

## T-App development

```mmm = loadModule("mmm", *args)```
:   load supporting TF-app specific module
:   `tf.applib.find.loadModule`

```~/mypath/app-myname/code/config.yaml```
:   settings for a TF-App
:   [app-default](https://github.com/annotation/app-default/blob/master/code/config.yaml)
