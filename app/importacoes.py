from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash,Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from aluno import Aluno
from diariobordo import DiarioBordo
from datetime import datetime
from gtts import gTTS
from textblob import TextBlob
from googletrans import Translator
import os
import urllib.parse