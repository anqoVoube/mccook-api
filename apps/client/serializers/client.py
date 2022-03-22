from rest_framework import serializers
from apps.client.models.client import User, Client
from email_validator import EmailNotValidError, validate_email
from django.db import transaction
from apps.client.password_validator import PasswordValidator
from apps.commentrate.models.commentrate import CommentRate
from apps.commentrate.serializers.commentrate import CommentrateSerializer


class UserSerializer(serializers.ModelSerializer):
    set_password  = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
        )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'set_password', 'confirm_password',
                  'special_question', 'special_answer']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def to_internal_value(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('set_password')
        confirm_password = data.get('confirm_password')
        first_name = str(data.get('first_name'))
        last_name = str(data.get('last_name'))
        special_question = data.get('special_question')
        special_answer = data.get('special_answer')
        
        dictionary_errors = {}

        if str(username).find('@') != -1:
            message = 'You can\'t use symbol \'@\' in \
your username field'
            dictionary_errors['wrong-symbol'] = [message]

        if len(username) < 3:
            message = 'The length of your username \
must contain at least 3 letters.'
            dictionary_errors['username-length'] = [message]

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            dictionary_errors['invalid-email'] = [str(e)]

        if password != confirm_password:
            message = "Passwords didn't match"
            dictionary_errors['password'] = [message]
        else:
            password_validation = PasswordValidator(password)
            response = password_validation\
                        .minlength(8)\
                            .maxlength(30)\
                                .has_lowercase()\
                                    .has_uppercase()\
                                        .get_response()
            dictionary_errors.update(response)
        if len(first_name) <= 1 or str(first_name).isalpha() == False:
            message = "Please provide your real name, so the people \
could find you. This field must have only english letters."

            dictionary_errors['fname-error'] = [message]

        if len(last_name) <= 1 or str(last_name).isalpha() == False:
            message = "Please provide your real last name, \
so the people could find you. \
This field must have only english letters."
            dictionary_errors['lname-error'] = [message]

        if User.objects.filter(email=email).exists():
            message = 'This email is already taken'
            dictionary_errors['email'] = [message]

        if User.objects.filter(username=username).exists(): 
            message = 'This username is already taken'
            dictionary_errors['username'] = [message]
        
        if ((special_question is None) and 
                (special_answer is not None)) or (
            (special_question is not None) and 
                (special_answer is None)
            ):
            message = "One field was assigned, however second was\'nt."
            dictionary_errors['notwo_null'] = [message]
        elif (special_question is not None) and (special_answer is not None):
            if len(special_answer) <= 2:
                message = "The secret answer must contain \
at least three letters or numbers"
                dictionary_errors['answer_length'] = [message]

        if dictionary_errors:
            raise serializers.ValidationError(dictionary_errors)

        return {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'set_password': password,
                'special_question': special_question,
                'special_answer': special_answer         
        }

    def validate(self, attrs):
        first_name = str(attrs.get('first_name')).capitalize()
        last_name = str(attrs.get('last_name')).capitalize()
        special_answer = attrs.get('special_answer')
        if special_answer is not None:
            special_answer = str(special_answer).capitalize()
            attrs["special_answer"] = special_answer

        attrs["first_name"] = first_name
        attrs["last_name"] = last_name
        return attrs
            
    @transaction.atomic
    def save(self):
        validated_data = self.validated_data
        password = validated_data['set_password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        special_question = validated_data['special_question']
        special_answer = validated_data['special_answer']
        try:
            user = User(first_name=first_name, 
                        last_name=last_name,
                        email=email, username=username, 
                        special_question=special_question,
                        special_answer=special_answer)
        except:
            message = "Error occured while registration, please try later"
            raise serializers.ValidationError({"error": [message]})

        user.set_password(password)
        user.save()


class ClientRetrieveSerializer(serializers.ModelSerializer):
    client_user = serializers.StringRelatedField()
    rating = serializers.SerializerMethodField()
    comments_rates = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ['client_user', 'rating', 'comments_rates'] # , 'favorite_recipes'

    def get_rating(self, obj):
        overall_stars = obj.overall_stars
        overall_rated = obj.overall_rated
        if overall_rated == 0 or overall_rated == 0:
            return 0
        return round((overall_stars / overall_rated), 2) # +Validation neeeded
        # 1 <= round <= 5
    
    def get_comments_rates(self, obj):
        comment_queryset = CommentRate.objects.filter(to_client=obj)
        serialized_data = CommentrateSerializer(
            comment_queryset, many=True).data
        return serialized_data
