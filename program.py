import sympy as sp
import re 

# Değişkenlerin tanımlanması
t, s = sp.symbols('t s')
X = sp.Function('X')(t)

# Kullanıcıdan diferansiyel denklemi alma
denklem = input("Diferansiyel denklemi giriniz (örn. X'' - 6*X' + 9*X): ")

denklem = denklem.replace("''", ".diff(t, 2)")  
denklem = denklem.replace("'", ".diff(t)") 
denklem = denklem.replace("x", "X") 
denklem = eval(denklem)

try:
    denklem = sp.sympify(denklem)

    X0 = 2
    X0_prime = -4

    # Laplace dönüşümünü alma
    laplace_eq = sp.laplace_transform(denklem, t, s, noconds=False)

    # Laplace dönüşümde başlangıç değerlerini yerine koyma
    laplace_eq_with_initials = laplace_eq[0].subs({
        sp.laplace_transform(X.diff(t), t, s)[0]: s * sp.Function('X')(s) - X0,
        sp.laplace_transform(X.diff(t, 2), t, s)[0]: s**2 * sp.Function('X')(s) - s * X0 - X0_prime
    })

    print("\nLaplace dönüşümü sonucu:")
    print(laplace_eq_with_initials)

    # Çözüme ulaşmak için bilinmeyen X(s)'i izole etme
    Xs = sp.solve(laplace_eq_with_initials, sp.Function('X')(s))

    # Eğer çözüm bulamazsa hata mesajı vermek
    if len(Xs) == 0:
        print("Denklem çözümlenemedi.")
    else:
        print("\nX(s) çözümü:")
        print(Xs[0])

        # Ters Laplace dönüşümü alarak X(t)'yi elde ediyoruz
        X_t = sp.inverse_laplace_transform(Xs[0], s, t)

        print("\nTers Laplace dönüşümü ile elde edilen X(t):")
        print(X_t)

except sp.SympifyError as e:
    print("Denklem işlenirken bir hata oluştu. Lütfen doğru bir formatta girdiğinizden emin olun.")
    print("Hata mesajı:", e)
except Exception as e:
    print("Bir hata oluştu:", e)
