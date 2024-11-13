# CHANGELOG


## v0.2.1 (2024-11-13)

### Chores

* chore: add more tests ([`4a3752e`](https://github.com/Kurrawong/rdfdig/commit/4a3752e40cfb276bbd57c168622e31298fc9c214))

* chore: update readme ([`c89ef7f`](https://github.com/Kurrawong/rdfdig/commit/c89ef7fc9f63bc274f3e71409ab7dd7c29749edc))

* chore: add more logging statements ([`8099f81`](https://github.com/Kurrawong/rdfdig/commit/8099f81e370d5d1fcbe2ed14ab4310b7254609e1))

### Fixes

* fix: relax python version requirements ([`87728f7`](https://github.com/Kurrawong/rdfdig/commit/87728f775568536b18b1518b08d79cb05cfbcbe5))


## v0.2.0 (2024-10-15)

### Chores

* chore: make errors print in red ([`65dbe1f`](https://github.com/Kurrawong/rdfdig/commit/65dbe1fd651c0c728c20125b9a516764584af7b2))

### Features

* feat: add support for sparql settings

allows setting the limit, offset, cutoff and timeout for sparql queries
when loading from remote sparql endpoint. ([`0445e6b`](https://github.com/Kurrawong/rdfdig/commit/0445e6b558a95cd15a27c39d0335db7ff137571d))

### Fixes

* fix: default to POST and fallback to GET on 405

to overcome errors from some services that only support one or the other
method ([`3fa9c0b`](https://github.com/Kurrawong/rdfdig/commit/3fa9c0bf5ea551efbb32a537fa6fbb6d26a9fefc))


## v0.1.1 (2024-10-14)

### Fixes

* fix: script declaration

config section was incorrect ([`72d48bd`](https://github.com/Kurrawong/rdfdig/commit/72d48bda5a84638b861ad81182a62bebf2ae4c32))


## v0.1.0 (2024-10-14)

### Chores

* chore: ignore ide files ([`d21e8e1`](https://github.com/Kurrawong/rdfdig/commit/d21e8e1370fb6872c064b170bb778b7b37ed584c))

* chore: test docstrings ([`810f85a`](https://github.com/Kurrawong/rdfdig/commit/810f85a298b96bdcdc875de1ad5b7265bb2a4f7a))

* chore: minimal test suite ([`bde3c00`](https://github.com/Kurrawong/rdfdig/commit/bde3c00eac16797015361c2ac5e34cfe8dc6ea86))

* chore: tidy up ([`b2e9b1c`](https://github.com/Kurrawong/rdfdig/commit/b2e9b1c0383863837fb6890824cbe3db226d1574))

* chore: update gitignore ([`ba741cf`](https://github.com/Kurrawong/rdfdig/commit/ba741cfa72fd958d257aa2ad9df421eeeaa842d9))

* chore: add better logs

improve the logging setup ([`4fcd07f`](https://github.com/Kurrawong/rdfdig/commit/4fcd07f55181a7517794af9a5e08859ea0b43b3d))

* chore: styling improvements ([`bf64d5d`](https://github.com/Kurrawong/rdfdig/commit/bf64d5d437fc2687c922cc7e9a2ace39a2274923))

* chore: docstrings

add documentation via docstrings ([`d6fb7ec`](https://github.com/Kurrawong/rdfdig/commit/d6fb7ec7a9b649fe2b7e25ab62f5448354752f38))

* chore: improve visjs rendering ([`779ff31`](https://github.com/Kurrawong/rdfdig/commit/779ff315b0de1598dae3be2e80ea8624b1956cd4))

* chore: small fixes

correct version number, add comments for Diagram internal properties,
remove options from the serialized visjs object help message ([`7e90e1b`](https://github.com/Kurrawong/rdfdig/commit/7e90e1be7d98af64a44f63b985c2913dcaff5ada))

* chore: mvp ([`711f058`](https://github.com/Kurrawong/rdfdig/commit/711f058363b4aa3835b5aa8cba84db3620a05e8d))

### Continuous Integration

* ci: remove pypi step ([`b7cb866`](https://github.com/Kurrawong/rdfdig/commit/b7cb86681c88fa90ae26d3e039c465db4cac17c3))

* ci: update release workflow ([`cd4538e`](https://github.com/Kurrawong/rdfdig/commit/cd4538e90ddef79b5b8a0dec966c03cb53504cd7))

### Documentation

* docs: update readme ([`4cf60e1`](https://github.com/Kurrawong/rdfdig/commit/4cf60e1fa2b166ca0925fad4cd389aa14a1e6b8d))

* docs: update readme.md ([`8946ee5`](https://github.com/Kurrawong/rdfdig/commit/8946ee5c14e85144b4e6db1e0b5959a27fe1df7b))

* docs: Update README.md ([`6c40d41`](https://github.com/Kurrawong/rdfdig/commit/6c40d415f3496d793d6f33de341d5c3621f3baf8))

* docs: update the readme ([`c005432`](https://github.com/Kurrawong/rdfdig/commit/c0054322d45415133e05a0d9277b96faf85fb587))

* docs: add license ([`88ddd4b`](https://github.com/Kurrawong/rdfdig/commit/88ddd4b673b588ac7c5d580c08818a3eb69758a4))

### Features

* feat: add support for mermaid

mvp for mermaid renderer. improvements could be done. ([`bd5ef0c`](https://github.com/Kurrawong/rdfdig/commit/bd5ef0c937d6d305028347e8918e140623a9ca67))

* feat: implement sparql loader

RDFDig can now read from remote sparql endpoints. including those
protected with HTTP Basic auth ([`97b29ea`](https://github.com/Kurrawong/rdfdig/commit/97b29eaec016751e8d313fd0b6dc51e32a9c8886))

* feat: instance level diagrams

add support for the iri argument to generate instance level diagrams ([`4264c17`](https://github.com/Kurrawong/rdfdig/commit/4264c1730a73b169509ad5fc05213366c611317f))

### Fixes

* fix: version reporting bug

previous implementation was causing an error when pip installed as
pyproj is not available. ([`d0d53da`](https://github.com/Kurrawong/rdfdig/commit/d0d53da625a14799029e6c940a2e59828306330e))

* fix: align version number with latest release ([`f94a364`](https://github.com/Kurrawong/rdfdig/commit/f94a364b1128ec9222793413de624d3a0774b990))

* fix: recursively load from folder

previous implentation could not handle subfolders and would cause an
error ([`9127183`](https://github.com/Kurrawong/rdfdig/commit/9127183ee3e6107b00fdec3e322fc1da4fe76a54))

* fix: sparql loader bnodes

add support for retrieving bnode properties to a depth of two. this is
now the default behaviour ([`43b45cb`](https://github.com/Kurrawong/rdfdig/commit/43b45cb643f1a95efb0f077cce26d2f43878ca57))

* fix: file and dir loaders not recieving a Path object

they were getting a string instead of a Path which is not what they were
expecting ([`e950820`](https://github.com/Kurrawong/rdfdig/commit/e9508205b1800ecaeba621334239419a5c0a5e25))

* fix: implement logic for iri flag in sparql loader

it was accidently ignored previously ([`558d711`](https://github.com/Kurrawong/rdfdig/commit/558d711c92d6d1c35264139d1d9fa11f23dcb05e))


## v0.0.0 (2024-08-22)

### Chores

* chore: update package description ([`1aedd27`](https://github.com/Kurrawong/rdfdig/commit/1aedd27188b74b413cea7ada6aa4b0405ed65911))

* chore: add a readme ([`4faccda`](https://github.com/Kurrawong/rdfdig/commit/4faccdaf26e730386b02a3bbf90d4f43e1897d50))

* chore: init ([`80efe64`](https://github.com/Kurrawong/rdfdig/commit/80efe64f08f99bab6dadd89c9fa0dc1927629dd4))

### Continuous Integration

* ci: add semantic-release workflow ([`418323d`](https://github.com/Kurrawong/rdfdig/commit/418323dcef6783380a5736b66193faa57b5f468a))
