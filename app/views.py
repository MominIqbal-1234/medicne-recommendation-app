
        
from django.shortcuts import render,HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.templatetags.static import static
from app import MedRecom
from django.conf import settings
import os
import ast
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin







class Login(View):
    def get(self,request):
        
        return render(request,'login.html')
    
    def post(slef,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('/') 
        

class Signup(View):
    def get(self,request):
        
        return render(request,'signup.html')
    def post(self,request):
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password,email=email)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('signup')
        else:
            messages.error(request, 'Passwords do not match!')
            return render(request,'signup.html')
        


class Home(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
            
        return render(request,'index.html')



class MedicineRecommendation(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        context = {}
        try:
            if request.session["True"] ==  True:
                context = {
                "data":True
            }
        except:
            pass
        return render(request,'medicine_recommendation.html',context)
    def post(self,request):
      
       
        symptoms = request.POST['symptoms']
        df_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'Training.csv')
        sym_des_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'symtoms_df.csv')
        precautions_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'precautions_df.csv')
        workout_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'workout_df.csv')
        description_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'description.csv')
        medications_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'medications.csv')
        diets_path = os.path.join(settings.BASE_DIR, 'static', 'archive', 'diets.csv')
        data = MedRecom.medRecom(
            symptoms,
            df_path,
            sym_des_path,
             precautions_path,
             workout_path,
             description_path,
             medications_path,
             diets_path
            )
        
        



        request.session["predicted_disease"] =  data[6]
        request.session["description"] =  data[1]
        request.session["precautions"] =  list(data[2][0])
        request.session["medications"] =  list(data[3])
        request.session["diets"] =  list(data[4])
        request.session["workout"] =  list(data[5])
        request.session["prognosis"] =  list(data[0])
        request.session["models_name_matrix"] =  list(data[7])
        request.session["total_number_of_unique_disease"] =  (data[8])
        request.session["True"] =  True

        context = {
            "data":True
        }
        return render(request,'medicine_recommendation.html',context=context)






class PredictedDisease(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        return render(request,'predicted_disease.html')


class Description(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        return render(request,'description.html')


class Precautions(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        data = request.session["precautions"] 
        print(data)
        context = {
            "data":data
        }
        return render(request,'precautions.html',context)

class Medications(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        data = request.session["medications"] 
        print(data)
        data = ast.literal_eval(data[0])
        context = {
            "data":data
        }
        return render(request,'medications.html',context)

class Diets(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        data = request.session["diets"] 
        print(data)
        data = ast.literal_eval(data[0])
        context = {
            "data":data
        }
        return render(request,'diets.html',context)

class Workout(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        data = request.session["workout"] 
        print(data)
        context = {
            "data":data
        }
        return render(request,'workout.html',context)


class DiseaseListDataset(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        data = request.session["prognosis"] 
        print(data)
        context = {
            "data":data
        }
        return render(request,'disease_list_dataset.html',context)


class Matrix(View):
    def get(self,request,model_name):
        if request.user.is_anonymous:
            return redirect("/")
        data = request.session["models_name_matrix"] 
        print(data[4])
        context = {}
        if model_name == "SVC":
            context = {
                "data":data[0]['SVC'],
                "model_name":'SVC'
            }
        elif model_name == "RandomForest":
            context = {
                "data":data[1]['Random Forest'],
                "model_name":'Random Forest'
            }
        elif model_name == "KNeighbors":
            context = {
                "data":data[2]['KNeighbors'],
                "model_name":'KNeighbors'
            }
        elif model_name == "GradientBoosting":
            context = {
                "data":data[3]['Gradient Boosting'],
                "model_name":'Gradient Boosting'
            }
        elif model_name == "MultinomialNB":
            context = {
                "data":data[4]['MultinomialNB'],
                "model_name":'MultinomialNB'
            }
        return render(request,'models_name_matrix.html',context)


class Logout(View):
    def get(self,request):
        logout(request)  
        return redirect('/')

class TotalNumberofUniqueDisease(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect("/")
        return render(request,'total_number_of_unique_disease.html')


class ModelTrainingResults(View):
    def get(self,request):
        data = ""
        if request.user.is_anonymous:
            return redirect("/")
        try:

            data = request.session["True"]
        except:
            data = False
        context = {
            "data":data
        }
        return render(request,'ModelTrainingResults.html',context)