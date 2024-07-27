import requests, datetime

icon_recommendations = {
    "PYQ": ["fa-solid fa-clock-rotate-left", "fa-solid fa-archive"],
    "Notes": ["fa-solid fa-note-sticky", "fa-solid fa-pen-to-square"],
    "Quiz": ["fa-solid fa-question-circle", "fa-solid fa-clipboard-question"],
    "Subject": ["fa-solid fa-book", "fa-solid fa-graduation-cap"],
    "Chapter": ["fa-solid fa-bookmark", "fa-solid fa-file-lines"],
    # Additional icons that might be useful
    "Home": ["fa-solid fa-home", "fa-solid fa-house"],
    "User": ["fa-solid fa-user", "fa-solid fa-user-circle"],
    "Settings": ["fa-solid fa-gear", "fa-solid fa-cog"],
    "Search": ["fa-solid fa-search", "fa-solid fa-magnifying-glass"],
    "Dashboard": ["fa-solid fa-chart-line", "fa-solid fa-tachometer-alt"],
    "Logout": ["fa-solid fa-right-from-bracket", "fa-solid fa-sign-out-alt"],
    "Login": ["fa-solid fa-right-to-bracket", "fa-solid fa-sign-in-alt"],
    "Profile": ["fa-solid fa-user-circle", "fa-solid fa-id-card"],
    "Notifications": ["fa-solid fa-bell", "fa-solid fa-envelope"],
    "Help": ["fa-solid fa-circle-question", "fa-solid fa-life-ring"],
    "Edit": ["fa-solid fa-pen-to-square", "fa-solid fa-edit"],
    "Delete": ["fa-solid fa-trash", "fa-solid fa-trash-alt"],
    "Add": ["fa-solid fa-plus", "fa-solid fa-circle-plus"],
    "Calendar": ["fa-solid fa-calendar", "fa-regular fa-calendar-days"],
    "Download": ["fa-solid fa-download", "fa-solid fa-cloud-arrow-down"],
    "Upload": ["fa-solid fa-upload", "fa-solid fa-cloud-arrow-up"],
    "List": ["fa-solid fa-list", "fa-solid fa-list-ul"],
    "Grid": ["fa-solid fa-grid", "fa-solid fa-th-large"],
    "Table": ["fa-solid fa-table", "fa-solid fa-table-cells"],
    "Chart": ["fa-solid fa-chart-bar", "fa-solid fa-chart-pie"],
    "File": ["fa-solid fa-file", "fa-regular fa-file"],
    "Folder": ["fa-solid fa-folder", "fa-regular fa-folder-open"],
    "Link": ["fa-solid fa-link", "fa-solid fa-chain"],
    "Star": ["fa-solid fa-star", "fa-regular fa-star"],
    "Heart": ["fa-solid fa-heart", "fa-regular fa-heart"],
    "Comment": ["fa-solid fa-comment", "fa-regular fa-comment-dots"],
    "Share": ["fa-solid fa-share", "fa-solid fa-share-nodes"],
    "Print": ["fa-solid fa-print", "fa-solid fa-printer"],
    "Lock": ["fa-solid fa-lock", "fa-solid fa-lock-closed"],
    "Unlock": ["fa-solid fa-unlock", "fa-solid fa-lock-open"],
    "Filter": ["fa-solid fa-filter", "fa-solid fa-sliders"],
    "Sort": ["fa-solid fa-sort", "fa-solid fa-arrow-up-wide-short"],
    "Refresh": ["fa-solid fa-rotate", "fa-solid fa-arrows-rotate"],
    "Info": ["fa-solid fa-circle-info", "fa-solid fa-info-circle"],
    "Warning": ["fa-solid fa-triangle-exclamation", "fa-solid fa-exclamation-triangle"],
    "Error": ["fa-solid fa-circle-xmark", "fa-solid fa-times-circle"],
    "Success": ["fa-solid fa-circle-check", "fa-solid fa-check-circle"]
}

icon_recommendations_using = {
    "pyq": ["fa-solid fa-clock-rotate-left", "fa-solid fa-archive"],
    "notes": ["fa-solid fa-note-sticky", "fa-solid fa-pen-to-square"],
    "quiz": ["fa-solid fa-question-circle", "fa-solid fa-clipboard-question"],
    "subject": ["fa-solid fa-book", "fa-solid fa-graduation-cap"],
    "chapter": ["fa-solid fa-bookmark", "fa-solid fa-file-lines"],
    "about": ["fa-solid fa-info-circle", "fa-solid fa-user"],
    "schoolstuff": ["fa-solid fa-graduation-cap","fa-solid fa-school"]
}
def get_internet_datetime(time_zone: str = "Asia/Kolkata"):
    """
    Get the current internet time from:
    'https://www.timeapi.io/api/Time/current/zone?timeZone=etc/utc'
    """
    timeapi_url = "https://www.timeapi.io/api/Time/current/zone"
    timeapi_url = f"http://worldtimeapi.org/api/timezone/{time_zone}"
    headers = {
        "Accept": "application/json",
    }
    request = requests.get(timeapi_url, headers=headers, timeout=120)
    r_dict = request.json()
    return r_dict