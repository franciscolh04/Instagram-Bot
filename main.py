## INSTAGRAM GROWER BOT ##

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

# DADOS DE ACESSO DA CONTA A UTILIZAR
myUsername = "" # CHANGE
myPassword = "" # CHANGE

# CAMINHO PARA O DRIVER DO BROWSER
PATH = "" #CHANGE
driver = webdriver.Chrome(PATH)

def wait(min, max):
    # Espera um tempo aleatório entre os limites especificados
    random_time = random.uniform(min, max)
    time.sleep(random_time)

def openInstagram():
    # Abre site
    driver.get("https://instagram.com/")

    # Permite cookies
    time.sleep(2)
    cookies = driver.find_element_by_xpath("/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]")
    cookies.send_keys(Keys.RETURN)

def login():
    # Entra na conta e nega notificações
    time.sleep(2)
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    login = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button")

    username.send_keys(myUsername)
    password.send_keys(myPassword)
    login.click()

    time.sleep(10)
    save = driver.find_element_by_xpath("//*[text()='Agora Não']")
    save.click()
    time.sleep(7)

    try:
        notif = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")
        notif.click()
    except:
        pass

def addFollowers(account):
     # Verifica o número de linhas no documento
    with open("./Instagram-Bot/toFollow.txt", "r") as file:
        number_of_lines = len(file.readlines())
    
    if (number_of_lines) <= 500:
        # Faz lista com pessoas a seguir
        driver.get("https://instagram.com/" + account)
        time.sleep(6)
        followers = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a")
        followers.click()

        time.sleep(2)
        followers_list = driver.find_element_by_css_selector("div._aano")

        # Dá scroll várias vezes para a lista de nomes aumentar
        for i in range (12):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", followers_list)
            wait(3, 5)

        usernames_list = driver.find_elements_by_css_selector('span._aacl._aaco._aacw._aacx._aad7._aade')

        # Lê os nomes de usuário já existentes no documento
        with open("./Instagram-Bot/toFollow.txt", "r") as file:
            usernames_existentes = [linha.strip() for linha in file.readlines()]

        # Abre o documento para adicionar novos nomes de utilizador
        with open("./Instagram-Bot/toFollow.txt", "a") as file:
                for i in usernames_list:
                    if i.text != myUsername:
                        if i.text not in usernames_existentes:
                            print("Vai escrever: " + i.text)
                            file.write(i.text + "\n")
                        else:
                            print("Já existe: " + i.text)
                    else:
                        print("Não é possível adicionar a minha conta: " + myUsername)
    else:
        print("Demasiadas contas já adicionadas: " + str(number_of_lines))

def isMemePage(account):
    #Verifica o nome de utilizador da conta
    if "meme" in account:
        print("Conta de memes encontrada: " + account)
        return True

    #Abre a página da conta e verifica a biografia da mesma
    driver.get("https://instagram.com/" + account)
    wait(1,3)
    try:
        bio = driver.find_element_by_css_selector('h1._aacl._aaco._aacu._aacx._aad6._aade')
        if "meme" in bio.text.lower():
            print("Conta de memes encontrada: " + account)
            return True
    except:
        pass

    return False


def addAccounts():
    # Lê os nomes de usuário já existentes no documento
    with open("./Instagram-Bot/toFollow.txt", "r") as file:
        # Verifica o número de linhas no documento
        number_of_lines = len(file.readlines())
    
    if number_of_lines <= 500:
        with open("./Instagram-Bot/toFollow.txt", "r") as file:
            usernames_existentes = [linha.strip() for linha in file.readlines()]

        # Verifica se as contas já adicionadas são contas de memes e, nesse caso,
        # se for conta pública, adiciona alguns dos seus seguidores à lista de pessoas a seguir
        for account in usernames_existentes:
            if isMemePage(account):
                try:
                    addFollowers(account)
                except:
                    print("Conta privada: " + account)
            wait(2,4)
    else:
        print("Demasiadas contas já adicionadas: " + str(number_of_lines))

def addAccount(account):
    # Abre o documento de contas a deixar de seguir e adiciona o nome de utilizador
    with open("./Instagram-Bot/toUnfollow.txt", "a") as file:
        file.write(account + "\n")


def removeAccount(account, filename):
    # Abre o documento do qual se pretende retirar o nome de utilizador
    with open("./Instagram-Bot/" + filename + ".txt", "r") as file:
        usernames = [linha.strip() for linha in file.readlines()]

    # Remove o nome de utilizador da lista se estiver presente
    if account in usernames:
        usernames.remove(account)

    # Escreve a lista atualizada de nomes de utilizador
    with open("./Instagram-Bot/" + filename + ".txt", "w") as file:
        for username in usernames:
            file.writelines(username + "\n")
    

def followAccount(account):
    # Abre a página da conta e, caso ainda não a siga, segue
    driver.get("https://instagram.com/" + account)
    wait(4,6)

    follow = driver.find_element_by_css_selector('._aacl._aaco._aacw._aad6._aade')
    if (follow.text == "Seguir"):
        # Segue a conta
        follow.click()
        wait(3,6)
        print("Seguiu: " + account)

        # Remove a conta do documento de contas a seguir e adiciona ao
        # documento de contas a deixar de seguir
        removeAccount(account, "toFollow")
        addAccount(account)
        wait(1,3)

        return True
    
    wait(3,5)
    return False

def unfollowAccount(account):
    # Abre a página da conta e, caso a siga ou tenha pedido enviado, deixa de o fazer
    driver.get("https://instagram.com/" + account)
    wait(4,6)

    follow = driver.find_element_by_css_selector('._aacl._aaco._aacw._aad6._aade')
    if follow.text in ("A seguir", "Pedido enviado"):
        # Deixa de seguir a conta
        follow.click()
        wait(3,6)
        
        confirm = driver.find_element_by_xpath("//*[text()='Não seguir']")
        confirm.click()
        print("Deixou de seguir: " + account)

        # Remove a conta do documento de contas a deixar de seguir
        removeAccount(account, "toUnfollow")
        wait(1,3)

        return True
    
    wait(3,5)
    return False

def follow(number):
    # Obtém n nomes de utilizador a seguir
    with open("./Instagram-Bot/toFollow.txt", "r") as file:
        accounts = [linha.strip() for linha in file.readlines()]

    cont = 0
    # Segue cada um deles
    for account in accounts:
        if cont < number:
            followed = followAccount(account)
            if followed:

                cont += 1
        else:
            break
    print("Seguiu contas: " + str(cont))
    

def unfollow(number):
    # Obtém n nome de utilizador a deixar de seguir
    with open("./Instagram-Bot/toUnfollow.txt", "r") as file:
        accounts = [linha.strip() for linha in file.readlines()]

    cont = 0
    # Deixa de seguir cada um deles
    for account in accounts:
        if cont < number:
            unfollowed = unfollowAccount(account)
            if unfollowed:
                cont += 1
        else:
            break
    print("Deixou de seguir contas: " + str(cont))


# Utilização das funções criadas de maneira a que o bot não seja detetado
def loop():
    openInstagram()
    login()
    addFollowers("") # CHANGE
    addAccounts()
    follow(15)
    time.sleep(3695)
    follow(60)
    time.sleep(3660)
    unfollow(60)
    time.sleep(3524)
    unfollow(47)


loop()

