from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import Category, Quiz, Question, Option, Attempt, Answer, UserProfile
from .serializers import CategorySerializer, QuizSerializer, QuestionSerializer, OptionSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Quiz, Attempt

@api_view(['GET'])
def welcome(request):
    """Welcome endpoint"""
    return Response({
        "message": "Welcome to Quiz API",
        "endpoints": {
            "register": "/api/register/",
            "login": "/api/login/",
            "quizzes": "/api/get-quizzes/",
            "questions": "/api/get-questions/<quiz_id>/",
            "options": "/api/get-options/"
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user=request.user
    all_quizzes= Quiz.objects.all()
    attempted_quizzes=Attempt.objects.filter(user=user)

    data = {
        'username': user.username,
        'email' : user.email,
        'is_staff': user.is_staff,
        'all_quizzes' :[
            { 'id': q.id, 'title': q.title,'description' :q.description}
            for q in all_quizzes
        ],
        'attempted_quizzes': [
            {
                'quiz_title' :a.quiz.title,
                'score':a.score,
                'attempted_on': a.completed_at,
            }
            for a in attempted_quizzes
            
        ],
    }
    return Response(data)



@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_quiz(request, pk):
    try:
        quiz = Quiz.objects.get(id=pk)
        serializer = QuizSerializer(quiz, context={'request': request})
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_quizzes(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_questions(request, quiz_id):
        questions = Question.objects.filter(quiz_id=quiz_id)
        data = []
        for q in questions:
            options = Option.objects.filter(question=q)  # or Option.objects.filter(question=q)
            data.append({
                'id': q.id,
                'text': q.question_text,

            })
        return Response(data)


@api_view(['GET'])
def get_option(request):
    """Get all options for quizzes - endpoint: /api/get-options/"""
    options = Option.objects.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        username: str = serializer.validated_data.get('username')  # type: ignore
        email: str = serializer.validated_data.get('email')  # type: ignore
        password: str = serializer.validated_data.get('password')  # type: ignore

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=user, role='student')
        token, created = Token.objects.get_or_create(user=user)

        return Response({"message": "Registration successful", "token": token.key}, status=201)

    # Format validation errors into a single message
    error_messages = []
    for field, errors in serializer.errors.items():  #type: ignore
        error_messages.append(f"{field}: {', '.join(str(e) for e in errors)}")
    error_message = " | ".join(error_messages) if error_messages else "Validation failed"
    
    return Response({"error": error_message}, status=400)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)
    
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)
    
    token, created = Token.objects.get_or_create(user=user)
    return Response({"message": "Login successful", "token": token.key}, status=200)

    if user is not None:
        login(request, user)
        return redirect('dashboard') 
    else:
        return render(request, 'login.html', {'error': 'Invalid credentials'})




@api_view(['post'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, quiz_id):
    user =request.user
    answers= request.data.get('answers')

    quiz= Quiz.objects.get(id=quiz_id)
    score = 0

    for  question_id, selected_option_id in answers.items():
        try:
            option = Option.objects.get(id=selected_option_id, question_id=question_id)
            if option.is_correct:
                score += 1
        except Option.DoesNotExist:
            continue

    attempt= Attempt.objects.create(user=user, quiz=quiz, score=score)

    return Response({
        'score':score,
        'total': Question.objects.filter(quiz=quiz).count(),
        'attempt_id': attempt.pk

    })