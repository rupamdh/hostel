from django.shortcuts import render, redirect
from .models import *
from account.models import User
from django.db import IntegrityError, transaction
from django.contrib import messages

# Create your views here.

