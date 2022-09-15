import os

# Regex patterns to ignore
ignored_patterns_list = [
    r"^node_modules$",
    r"^venv$",
    r"^env$",
    r"^\..*",
    r"^_.*",
    r"^obj$",
    r"^bin$",
    r"^build$",
    r"^cache$",
    r"^dist$",
    r"^temp$",
    r"^tmp$",
    r".*undo.*",
    r"^.*\.lproj$",
    r".*\.app$",
]

# Combine the regex patterns into one
IGNORED_FOLDERS = "(" + ")|(".join(ignored_patterns_list) + ")"

# Root directories to look in
ROOTS_TO_LOOK_IN = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music"),
    os.path.expanduser("~/Movies"),
    "/Applications",
]

# Files considered code
CODE_EXTENSIONS = set(
    [
        "py",
        "cpp",
        "c",
        "js",
        "ts",
        "html",
        "css",
        "scss",
        "sass",
        "less",
        "json",
        "md",
        "txt",
        "sh",
        "yaml",
        "yml",
        "xml",
        "java",
        "kt",
        "go",
        "rs",
        "rb",
        "php",
        "swift",
        "dart",
        "h",
    ]
)

# Files considered images
IMAGE_EXTENSIONS = set(
    [
        "png",
        "jpg",
        "jpeg",
        "gif",
        "svg",
        "bmp",
    ]
)
