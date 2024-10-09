from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash,Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
from gtts import gTTS
from textblob import TextBlob
from googletrans import Translator
from aluno import Aluno
from diariobordo import DiarioBordo
from funcioario import Funcionario
import os
import urllib.parse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS