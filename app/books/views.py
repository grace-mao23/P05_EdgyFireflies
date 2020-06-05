from flask import (Blueprint, session, redirect, url_for, request, flash,
                   render_template)

from app import db

bp = Blueprint("books",
               __name__,
               url_prefix="/books",
               template_folder="templates",
               static_folder="static")
