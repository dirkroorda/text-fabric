import sys
import os
from shutil import rmtree, copytree, copyfile

from subprocess import run, call, Popen, PIPE

import errno
import time
import unicodedata


SRC = "site"
REMOTE = "origin"
BRANCH = "gh-pages"


# COPIED FROM MKDOCS AND MODIFIED


def console(*args):
    sys.stderr.write(" ".join(args) + "\n")
    sys.stderr.flush()


def _enc(text):
    if isinstance(text, bytes):
        return text
    return text.encode()


def _dec(text):
    if isinstance(text, bytes):
        return text.decode("utf-8")
    return text


def _write(pipe, data):
    try:
        pipe.stdin.write(data)
    except OSError as e:
        if e.errno != errno.EPIPE:
            raise


def _normalize_path(path):
    # Fix unicode pathnames on OS X
    # See: https://stackoverflow.com/a/5582439/44289
    if sys.platform == "darwin":
        return unicodedata.normalize("NFKC", _dec(path))
    return path


def _try_rebase(remote, branch):
    cmd = ["git", "rev-list", "--max-count=1", "{}/{}".format(remote, branch)]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (rev, _) = p.communicate()
    if p.wait() != 0:
        return True
    cmd = ["git", "update-ref", "refs/heads/%s" % branch, _dec(rev.strip())]
    if call(cmd) != 0:
        return False
    return True


def _get_config(key):
    p = Popen(["git", "config", key], stdin=PIPE, stdout=PIPE)
    (value, _) = p.communicate()
    return value.decode("utf-8").strip()


def _get_prev_commit(branch):
    cmd = ["git", "rev-list", "--max-count=1", branch, "--"]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (rev, _) = p.communicate()
    if p.wait() != 0:
        return None
    return rev.decode("utf-8").strip()


def _mk_when(timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    currtz = "%+05d" % (-1 * time.timezone / 36)  # / 3600 * 100
    return "{} {}".format(timestamp, currtz)


def _start_commit(pipe, branch, message):
    uname = _dec(_get_config("user.name"))
    email = _dec(_get_config("user.email"))
    _write(pipe, _enc("commit refs/heads/%s\n" % branch))
    _write(pipe, _enc("committer {} <{}> {}\n".format(uname, email, _mk_when())))
    _write(pipe, _enc("data %d\n%s\n" % (len(message), message)))
    head = _get_prev_commit(branch)
    if head:
        _write(pipe, _enc("from %s\n" % head))
    _write(pipe, _enc("deleteall\n"))


def _add_file(pipe, srcpath, tgtpath):
    with open(srcpath, "rb") as handle:
        if os.access(srcpath, os.X_OK):
            _write(pipe, _enc("M 100755 inline %s\n" % tgtpath))
        else:
            _write(pipe, _enc("M 100644 inline %s\n" % tgtpath))
        data = handle.read()
        _write(pipe, _enc("data %d\n" % len(data)))
        _write(pipe, _enc(data))
        _write(pipe, _enc("\n"))


def _add_nojekyll(pipe):
    _write(pipe, _enc("M 100644 inline .nojekyll\n"))
    _write(pipe, _enc("data 0\n"))
    _write(pipe, _enc("\n"))


def _gitpath(fname):
    norm = os.path.normpath(fname)
    return "/".join(norm.split(os.path.sep))


def _ghp_import():
    if not _try_rebase(REMOTE, BRANCH):
        print("Failed to rebase %s branch.", BRANCH)

    console("copy docs to the gh-pages branch")
    cmd = ["git", "fast-import", "--date-format=raw", "--quiet"]
    kwargs = {"stdin": PIPE}
    if sys.version_info >= (3, 2, 0):
        kwargs["universal_newlines"] = False
    pipe = Popen(cmd, **kwargs)
    _start_commit(pipe, BRANCH, "docs update")
    for path, _, fnames in os.walk(SRC):
        for fn in fnames:
            fpath = os.path.join(path, fn)
            fpath = _normalize_path(fpath)
            gpath = _gitpath(os.path.relpath(fpath, start=SRC))
            _add_file(pipe, fpath, gpath)
    _add_nojekyll(pipe)
    _write(pipe, _enc("\n"))
    pipe.stdin.close()
    if pipe.wait() != 0:
        sys.stdout.write(_enc("Failed to process commit.\n"))

    console("push gh-pages branch to GitHub")
    cmd = ["git", "push", REMOTE, BRANCH]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    (out, err) = proc.communicate()
    result = proc.wait() == 0

    return result, _dec(err)


def _gh_deploy(org, repo):
    (result, error) = _ghp_import()
    if not result:
        print("Failed to deploy to GitHub with error: \n%s", error)
        raise SystemExit(1)
    else:
        url = f"https://{org}.github.io/{repo}/"
        print("Your documentation should shortly be available at: " + url)


# END COPIED FROM MKDOCS AND MODIFIED


PDOC3 = [
    "pdoc3",
    "--force",
    "--html",
    "--output-dir",
    "site",
    "--template-dir",
    "docs/templates",
]
PDOC3STR = " ".join(PDOC3)


def pdoc3serve(package):
    """Build the docs into site and serve them.
    """

    proc = Popen([*PDOC3, "--http", ":", package])
    time.sleep(1)
    run(f"open http://localhost:8080/{package}", shell=True)
    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    proc.terminate()


def pdoc3(package):
    """Build the docs into site.
    """

    console("Build docs")
    if os.path.exists("site"):
        console("Remove previous build (site)")
        rmtree("site")
    console("Generate docs with pdoc3")
    run(f"{PDOC3STR} {package}", shell=True)
    # console("Move docs into place")
    # run(f"mv site/{package}/* site", shell=True)
    # rmtree(f"site/{package}")
    # console("Copy over the images")
    copytree("docs/images", f"site/{package}/images", dirs_exist_ok=True)
    copyfile("docs/index.html", "site/index.html")


def shipDocs(org, repo, package):
    """Build the docs into site and ship them.
    """

    pdoc3(package)
    _gh_deploy(org, repo)
