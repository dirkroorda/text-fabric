import re
import types

from ..parameters import (
    URL_GH,
    URL_TFDOC,
    APP_URL,
    APP_NB_URL,
)
from ..core.helpers import htmlEsc
from .repo import Checkout
from .helpers import dh
from .display import getText


UNSUPPORTED = "not online"

pathRe = re.compile(
    r"^(.*/(?:github|text-fabric-data))/([^/]+)/([^/]+)/(.*)$", flags=re.I
)


def linksApi(app, silent):
    """Produce the link API.

    The link API provides methods to maps nodes to urls of web resources.
    It also computes several provenance and documentation links from the
    configuration settings of the corpus.

    Parameters
    ----------
    app: obj
        The high-level API object
    silent:
        The verbosity mode to perform this operation in.
        Normally it is the same as for the app, but when we do an `A.reuse()`
        we force `silent=True`.
    """
    app.header = types.MethodType(header, app)
    app.webLink = types.MethodType(webLink, app)
    isCompatible = app.isCompatible

    api = app.api

    aContext = app.context
    appName = aContext.appName
    docUrl = aContext.docUrl
    repo = aContext.repo
    version = aContext.version
    corpus = aContext.corpus
    featureBase = aContext.featureBase
    featurePage = aContext.featurePage
    charUrl = aContext.charUrl
    charText = aContext.charText

    tutUrl = f"{APP_NB_URL}/{appName}/start.ipynb"
    extraUrl = f"{APP_URL}/app-{appName}"

    dataLink = (
        outLink(repo.upper(), docUrl, f"provenance of {corpus}")
        if isCompatible and repo is not None and docUrl
        else UNSUPPORTED
    )
    charLink = (
        (
            outLink("Character table", charUrl.format(tfDoc=URL_TFDOC), charText)
            if isCompatible
            else UNSUPPORTED
        )
        if charUrl
        else ""
    )
    featureLink = (
        (
            outLink(
                "Feature docs",
                featureBase.replace("<feature>", featurePage).format(version=version),
                f"{repo.upper()} feature documentation",
            )
            if isCompatible and repo is not None and featureBase
            else UNSUPPORTED
        )
        if isCompatible
        else UNSUPPORTED
    )
    appLink = outLink(
        f"{appName} API",
        extraUrl,
        f"{appName} API documentation"
        if isCompatible and repo is not None
        else UNSUPPORTED,
    )
    tfLink = (
        outLink(
            f"Text-Fabric API {api.TF.version}",
            f"{URL_TFDOC}/Api/Fabric/",
            "text-fabric-api",
        )
        if isCompatible
        else UNSUPPORTED
    )
    tfsLink = (
        outLink(
            "Search Reference",
            f"{URL_TFDOC}/Use/Search/",
            "Search Templates Introduction and Reference",
        )
        if isCompatible
        else UNSUPPORTED
    )
    tutLink = (
        outLink("App tutorial", tutUrl, "App tutorial in Jupyter Notebook")
        if isCompatible and repo is not None
        else UNSUPPORTED
    )
    if app._browse:
        app.dataLink = dataLink
        app.charLink = charLink
        app.featureLink = featureLink
        app.tfsLink = tfsLink
        app.tutLink = tutLink
    else:
        if not silent:
            dh(
                "<b>Documentation:</b>"
                f" {dataLink} {charLink} {featureLink} {appLink} {tfLink} {tfsLink}"
                "<details open><summary><b>Loaded features</b>:</summary>\n"
                + _featuresPerModule(app)
                + "</details>"
            )


def header(app):
    """Generate a colofon of the TF-app.

    This colofon will be displayed after initializing the advanced API,
    and it is packed with provenance and documentation links.
    """

    return (
        f"""\
<div class="hdlinks">
  {app.dataLink}
  {app.charLink}
  {app.featureLink}
  {app.tfsLink}
  {app.tutLink}
</div>\
""",
        f'<img class="hdlogo" src="/data/static/logo.png"/>',
        f'<img class="hdlogo" src="/server/static/icon.png"/>',
    )


def webLink(
    app, n, text=None, clsName=None, urlOnly=False, _asString=False, _noUrl=False
):
    """Maps a node to a web resource.

    Usually called as `A.weblink(...)`

    The mapping is quite sophisticated. It will do sensible things for
    section nodes and lexeme nodes, dependent on how they are configured in
    the app's `config.yaml`.

    !!! hint "Customizable"
        You can customize the behaviour of `webLink()` to the needs of your corpus
        by providing appropriate values in its `config.yaml`, especially for
        `webBase`, `webLang`, `webUrl`, `webUrlLex`, and `webHint`.

    Parameters
    ----------
    app: object
        The `A`.
    n: int
        A node
    text: string/HTML, optional default `None`
        The text of the link. If left out, a suitable text will be derived from
        the node.
    clsName: string, optional default `None`
        A CSS class name to add to the resulting link element
    urlOnly: boolean, optional `False`
        If True, only the url will be returned.
    _asString: boolean, optional `False`
        Whether to deliver the result as a piece of HTML or to display the link
        on the (Jupyter) interface.
    _noUrl: boolean, optional `False`
        Whether to put the generated url in the `href` attribute.
        It can be inhibited. This is useful for the TF-browser, which may want
        to attach an action to the link and navigate to a location based on
        other attributes.
    """

    api = app.api
    T = api.T
    F = api.F
    Fs = api.Fs

    aContext = app.context
    webBase = aContext.webBase
    webLang = aContext.webLang
    webUrl = aContext.webUrl
    webUrlLex = aContext.webUrlLex
    webLexId = aContext.webLexId
    webHint = aContext.webHint
    lexTypes = aContext.lexTypes
    styles = aContext.styles

    nType = F.otype.v(n)
    passageText = None

    if nType in lexTypes:
        if text is None:
            text = getText(app, False, n, nType, False, True, True, "", None)
        if webUrlLex and webLexId:
            lid = (
                app.getLexId(n)
                if webLexId is True
                else Fs(webLexId).v(n)
                if webLexId
                else None
            )
            theUrl = webUrlLex.replace("<lid>", str(lid))
        elif webBase:
            theUrl = webBase
        else:
            theUrl = None
    else:
        if text is None:
            text = app.sectionStrFromNode(n)
            passageText = text
        if webUrl:
            theUrl = webUrl
            headingTuple = T.sectionFromNode(n, lang=webLang, fillup=True)
            for (i, heading) in enumerate(headingTuple):
                theUrl = theUrl.replace(f"<{i + 1}>", str(heading))
        else:
            theUrl = None

    style = styles.get(nType, None)
    if style:
        clsName = f"{clsName or ''} {style}"
    if theUrl is None:
        fullResult = text
        href = None
    else:
        href = "#" if _noUrl else theUrl
        atts = dict(target="") if _noUrl else dict(title=webHint)
        fullResult = outLink(text, href, clsName=clsName, passage=passageText, **atts,)
    result = href if urlOnly else fullResult
    if _asString or urlOnly:
        return result
    dh(result)


def outLink(text, href, title=None, passage=None, clsName=None, target="_blank"):
    """Produce a formatted link.

    Parameters
    ----------
    text: string/HTML
        The text of the link.
    href: string/URL
        The url of the link.
    title: string, optional `None`
        The hint of the link.
    target: string, optional `_blank`
        The target window/tab of the link.
    clsName: string, optional default `None`
        A CSS class name to add to the resulting link element
    passage: string, optional `None`
        A passage indicator, which will end up in the `sec` attribute of the
        link element. Used by the TF-browser.
    """

    titleAtt = "" if title is None else f' title="{title}"'
    clsAtt = f' class="{clsName.lower()}"' if clsName else ""
    targetAtt = f' target="{target}"' if target else ""
    passageAtt = f' sec="{passage}"' if passage else ""
    return (
        f'<a{clsAtt}{targetAtt} href="{htmlEsc(href)}"{titleAtt}{passageAtt}>'
        f"{text}</a>"
    )


def _featuresPerModule(app):
    """Generate a formatted list of loaded TF features, per module.
    """

    isCompatible = app.isCompatible
    if not isCompatible:
        return UNSUPPORTED

    api = app.api
    TF = api.TF

    aContext = app.context
    mOrg = aContext.org
    mRepo = aContext.repo
    mRelative = aContext.relative
    version = aContext.version
    moduleSpecs = aContext.moduleSpecs
    corpus = aContext.corpus
    featureBase = aContext.featureBase

    features = api.Fall() + api.Eall()

    fixedModuleIndex = {}
    for m in moduleSpecs or []:
        fixedModuleIndex[(m["org"], m["repo"], m["relative"])] = (
            m["corpus"],
            m["docUrl"],
        )

    moduleIndex = {}
    mLocations = app.mLocations if hasattr(app, "mLocations") else []
    baseLoc = mLocations[0] if hasattr(app, "mLocations") else ()

    for mLoc in mLocations:
        match = pathRe.fullmatch(mLoc)
        if not match:
            moduleIndex[mLoc] = ("??", "??", "??", mLoc, "")
        else:
            (base, org, repo, relative) = match.groups()
            mId = (org, repo, relative)
            (corpus, docUrl) = (
                (relative, None)
                if org is None or repo is None
                else (
                    (corpus, featureBase.format(version=version))
                    if featureBase
                    else (corpus, None)
                )
                if mLoc == baseLoc
                else fixedModuleIndex[mId]
                if mId in fixedModuleIndex
                else (
                    f"{org}/{repo}/{relative}",
                    f"{URL_GH}/{org}/{repo}/tree/master/{relative}",
                )
            )
            moduleIndex[mId] = (org, repo, relative, corpus, docUrl)

    featureCat = {}

    for feature in features:
        added = False
        featureInfo = TF.features[feature]
        featurePath = featureInfo.path
        match = pathRe.fullmatch(featurePath)
        if match:
            (base, fOrg, fRepo, relative) = match.groups()
            fRelative = relative.rsplit("/", 1)[0]
            mId = (fOrg, fRepo, fRelative)
        else:
            mId = featurePath.rsplit("/", 1)[0]
        if type(mId) is str:
            for (mIId, mInfo) in moduleIndex.items():
                if type(mIId) is str:
                    if featurePath.startswith(mIId):
                        featureCat.setdefault(mIId, []).append(feature)
                        added = True
        else:
            for (mIId, mInfo) in moduleIndex.items():
                if type(mIId) is not str:
                    (mOrg, mRepo, mRelative) = mIId
                    if (
                        fOrg == mOrg
                        and fRepo == mRepo
                        and fRelative.startswith(mRelative)
                    ):
                        featureCat.setdefault(mIId, []).append(feature)
                        added = True
        if not added:
            featureCat.setdefault(mId, []).append(feature)

    baseId = (mOrg, mRepo, mRelative)
    baseMods = {
        mId for mId in featureCat.keys() if type(mId) is tuple and mId == baseId
    }
    moduleOrder = list(baseMods) + sorted(
        (mId for mId in featureCat.keys() if mId not in baseMods),
        key=lambda mId: (1, mId) if type(mId) is str else (0, mId),
    )

    html = ""
    for mId in moduleOrder:
        catFeats = featureCat[mId]
        if not catFeats:
            continue
        modInfo = moduleIndex.get(mId, None)
        if modInfo:
            (org, repo, relative, corpus, docUrl) = modInfo
        else:
            corpus = mId if type(mId) is str else "/".join(mId)
            docUrl = (
                ""
                if type(mId) is str
                else f"{URL_GH}/{mId[0]}/{mId[1]}/tree/master/{mId[2]}"
            )
        html += f"<p><b>{corpus}</b>:"

        seen = set()

        for feature in catFeats:
            if "@" in feature:
                dlFeature = f'{feature.rsplit("@", 1)[0]}@ll'
                if dlFeature in seen:
                    continue
                seen.add(dlFeature)
                featureRep = dlFeature
            else:
                featureRep = feature
            featureInfo = TF.features[feature]
            featurePath = featureInfo.path
            isEdge = featureInfo.isEdge
            pre = "<b><i>" if isEdge else ""
            post = "</i></b>" if isEdge else ""
            html += f" {pre}"
            html += (
                outLink(
                    featureRep,
                    docUrl.replace("<feature>", featureRep),
                    title=featurePath,
                )
                if docUrl
                else f'<span title="{featurePath}">{featureRep}</span>'
            )
            html += f"{post} "
        html += "</p>"
    return html


def provenanceLink(org, repo, version, commit, release, local, relative):
    """Generate a provenance link for a data source.

    We assume the data source resides somewhere inside a GitHub repo.

    Parameters
    ----------
    org: string
        Organization on GitHub
    repo: string
        Repository on Github
    version: string
        Version of the data source.
        This is not the release or commit of a repo, but the subdirectory
        corresponding with a data version under a `tf` directory with feature files.
    commit: string
        The commit hash of the repository on GitHub.
    """

    text = (
        f"data on local machine {relative}"
        if org is None or repo is None
        else f"{org}/{repo} v:{version} ({Checkout.toString(commit, release, local)})"
    )
    relativeFlat = relative.replace("/", "-")
    url = (
        None
        if org is None or repo is None
        else f"{URL_GH}/{org}/{repo}/tree/master/{relative}"
        if local
        else (
            f"{URL_GH}/{org}/{repo}/releases/download/{release}"
            f"/{relativeFlat}-{version}.zip"
            if release
            else f"{URL_GH}/{org}/{repo}/tree/{commit}/{relative}"
        )
    )
    return (text, url)
