from django.http import HttpResponse
from django.shortcuts import render
from requests import get, post


def ifint(integer):
    integer = str(integer)
    lst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if integer == '':
         return False
    else:
        ifinteger = True
        for i in range(len(integer)):
            if integer[i] not in lst:
                ifinteger = False
        return(ifinteger)

def issimple(num):
    if num == 1:
        return False
    else:
        lst = list(range(0, num))
        i = 2
        while i < num:
            if lst[i] != 0:
                if num%lst[i] == 0:
                    return False
                for j in range(i, num, i):
                    lst[j] = 0
            i += 1
        return True

def nod(a, b):
        return(a%b == 0)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in list(range(3, int(num**0.5)+2, 2)):
        if num % n == 0:
            return False
    return True

def fast_mod(x, n, m):
    a = 1
    b = x
    while True:

        temp = n

        if n % 2 == 1:
            a = a * b % m

        b = b * b % m
        n = n // 2

        if temp < 1:
            return a

def find_special_number(n):
    num = 0 
    while num < n+1:
        if is_prime(num):
            if n%num != 0:
                e = num
                return e
        num += 1
                

def genkey(p, q):

    # generating keys

    n = p*q
    N = (p-1)*(q-1)

    e = 0 

    # finding special number
    e = find_special_number(N)
    d = mulinv(e, N)

    return(e, n, d, n)

def home(request):
    res=get_session_cache(request)
    return render(request, 'index.html', res)


def encode(e, n, text):
    # Converting texr 2 int
    splitext = []
    for char in text:
        splitext.append(str(ord(char)))

    # Encrypting text
    code = ''
    i = 0
    for char in splitext:
        m = int(char)
        code += str(fast_mod(m, e, n))
        code += ' '

    return code

def decode(e, n, code):
    # Decrypting text
    word = ''
    intext = []
    for char in code:
        m = int(char)
        intext.append(int(fast_mod(m, e, n)))

    # Converting int 2 text
    for char in intext:
        if not(char >= 65536):
            word += chr(char)
        else:
            return('False')
    return word

def get_session_cache(request):
    res={ 'open':request.session.get('open'),
             'closed':request.session.get('closed'),
            'first_num':request.session.get('first_num'),
             'second_num':request.session.get('second_num'),


            'first_close':request.session.get('first_close'),
             'second_close':request.session.get('second_close'),
            'encode_text':request.session.get('encode_text'),
             'to_encode_text': request.session.get('to_encode_text'),

            'first_open':request.session.get('first_open'),
             'second_open': request.session.get('second_open'),
            'to_decode_text': request.session.get('to_decode_text'),
             'decode_text': request.session.get('decode_text')}
    result = {k: v for k, v in res.items() if v is not None}
    return result


def contact_gen_key(request):
    error = ''
    frst = ''
    scnd = ''
    if request.POST:
        frst = request.POST.get('first_num')
        scnd = request.POST.get('second_num')
        if not(ifint(frst) and ifint(scnd)):
            error = 'Both numbers must be integer'
        else:
            frst = int(frst)
            scnd = int(scnd)
            if not(is_prime(frst) and is_prime(scnd)):
                error = 'Both numbers must be simple'
            if (frst < 200) or (scnd < 200):
                error = 'Both numbers must be more than 200'
        if scnd == '':
            error = 'Enter second number'
        if frst == '':
            error = 'Enter first number'
        if not error:
            keys = genkey(frst, scnd)
            openedkey = '{}, {}'.format(keys[0], keys[1])
            closedkey = '{}, {}'.format(keys[2], keys[3])

            request.session['open']=openedkey
            request.session['closed']=closedkey
            request.session['first_num']=frst
            request.session['second_num']=scnd
        else:
            request.session['open'] = None
            request.session['closed'] = None
            request.session['first_num'] = None
            request.session['second_num'] = None

    res=get_session_cache(request)
    if error:
        res['key_error']=error
    return render(request, 'index.html', res)





def encode_contact(request):
    error = ''
    text = ''
    key = ''
    frst = ''
    scnd = ''
    sep = ''
    code = ''
    if request.POST:        
        key = request.POST.get('encode_key')
        text = request.POST.get('to_encode_text')
        key = key.replace(',', '')
        keys = key.split()
        if len(keys) != 2:
            error = 'Key must contain 2 numbers'
        else:
            sep = ', '
            frst = keys[0]
            scnd = keys[1]
            if not(ifint(frst) and ifint(scnd)):
                error = 'Key numbers must be integer'
        if text == '':
            error = 'Enter your text'
        if key == '':
            error = 'Enter your keys'
        if not error:
            code = encode(int(frst), int(scnd), text)

            request.session['first_close']=frst+sep
            request.session['second_close']=scnd
            request.session['encode_text']=code
            request.session['to_encode_text']=text
        else:
            request.session['first_close'] = None
            request.session['second_close'] = None
            request.session['encode_text'] = None
            request.session['to_encode_text'] = None

    res = get_session_cache(request)
    if error:
        res['encode_error'] = error

    return render(request, 'index.html', res)




def decode_contact(request):
    error = ''
    text = ''
    key = ''
    frst = ''
    scnd = ''
    sep = ''
    code = ''
    if request.POST:        
        key = request.POST.get('decode_key')
        code = request.POST.get('to_decode_text')
        key = key.replace(',', '')
        keys = key.split()
        if not(ifint(code.replace(' ', ''))):
            error = 'Code must contain only numbers and spaces'
        if len(keys) != 2:
            error = 'Key must contain 2 numbers'
        else:
            sep = ', '
            frst = keys[0]
            scnd = keys[1]
            if not(ifint(frst) and ifint(scnd)):
                error = 'Key numbers must be integer'
        if code == '':
            error = 'Enter your code'
        if key == '':
            error = 'Enter your keys'
        if not error:
            text = decode(int(frst), int(scnd), code.split())
            if text == 'False':
                error = 'Error, wrong keys, or code'
                text = ''

            request.session['first_open'] = frst + sep
            request.session['second_open'] = scnd
            request.session['decode_text'] = text
            request.session['to_decode_text'] = code
        else:
            request.session['first_open'] = None
            request.session['second_open'] = None
            request.session['decode_text'] = None
            request.session['to_decode_text'] = None

    res = get_session_cache(request)
    if error:
        res['decode_error'] = error

    return render(request, 'index.html', res)

        


