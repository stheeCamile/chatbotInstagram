from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

class ReplyBot:
    def initialize_crawler(self, post_link, username, password, comment_text):
        self.post_link = post_link
        self.username = username
        self.password = password
        self.comment_text = comment_text

        path_user_data = str(Path('User Data').absolute())

        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir={}".format(path_user_data))
        driver = uc.Chrome(version_main=114, options=options)

        try:
            login = threading.Thread(target=self.login, args=(driver,))
            login.start()
            login.join()  # Aguarda a conclusão da thread de login
        except:
            print('Erro ao fazer login')

    def login(self, driver):
        try:
            driver.get('https://www.instagram.com/accounts/login/')
            driver.switch_to.new_window('tab')
            driver.get("https://chat.openai.com/")

            self.insta_window = driver.window_handles[0]
            self.chat_window = driver.window_handles[1]

            sleep(5)
            driver.switch_to.window(self.insta_window)

            username = driver.find_element(By.CSS_SELECTOR, 'form#loginForm input[name="username"]')
            username.click()
            username.send_keys(self.username)

            password = driver.find_element(By.CSS_SELECTOR, 'form#loginForm input[name="password"]')
            password.click()
            password.send_keys(self.password)

            submit = driver.find_element(By.CSS_SELECTOR, 'form#loginForm button[type="submit"]')
            submit.click()
            sleep(5)
        except:
            pass

        self.go_to_post(driver=driver)

    def go_to_post(self, driver):
        driver.get("https://www.instagram.com/p/{post_link}/".format(post_link=self.post_link))
        sleep(5)
        print('entrou no link')
        self.get_replys_list(driver=driver)

    def get_replys_list(self, driver: uc.Chrome):
        driver.switch_to.window(self.chat_window)
        driver.switch_to.window(self.insta_window)
        sleep(1)
        # Procura as divs dos comentários que não tenhos sido respondidos
        comment_elements = driver.find_elements(By.XPATH, '//div[./div/div/div/div/div/span[text()="Responder"] and not(following-sibling::div[1])]')
        for comment_element in comment_elements:
            # busca o elemento que contem o texto do comentario
            comment_text_element = comment_element.find_element(By.XPATH, './div/div[2]/div/div/div/div[2]/span')
            comment_text = comment_text_element.text
            print('Texto do comentário:', comment_text)
            self.reply_with_gpt(driver, comment_text, comment_element)
                
    def reply_with_gpt(self, driver: uc.Chrome, comment_text, comment_element):
        driver.switch_to.window(self.chat_window)
        
        textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))
        textarea.click()
        textarea.clear()
        textarea.send_keys(f'{comment_text}"')
        sleep(2)
        textarea.send_keys(Keys.ENTER)
        sleep(5)

        resposta_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.markdown.prose.w-full.break-words.dark\:prose-invert.light p"))
        )
        resposta_texto = resposta_element.text
                # Aguardar até que o botão "New chat" seja visível
        botao_new_chat = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mb-1.flex.flex-row.gap-2 > a'))
        )
        # Simular um clique com o mouse no botão "New chat"
        ActionChains(driver).move_to_element(botao_new_chat).click().perform()

        # Volta ao Facebook, aperta o botão de notificação
        driver.switch_to.window(self.insta_window)
        print('Resposta do comentário:', resposta_texto)
        # Responde ao comentário do Instagram com a resposta do ChatGPT
        self.reply_back(driver=driver, reply_text=resposta_texto, comment_element=comment_element)

    def reply_back(self, driver, reply_text, comment_element):
        sleep(3)
        # busca o botão "Responder"
        reply_button = comment_element.find_element(By.XPATH, './/div[@role="button"]')
        print('localizou o botão')
        reply_button.click()
        print('cliclou no botão')

        sleep(3)
        reply_textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.x1i0vuye.xvbhtw8.x76ihet.xwmqs3e.x112ta8.xxxdfa6.x5n08af.x78zum5.x1iyjqo2.x1qlqyl8.x1d6elog.xlk1fp6.x1a2a7pz.xexx8yu.x4uap5.x18d9i69.xkhd6sd.xtt52l0.xnalus7.xs3hnx8.x1bq4at4.xaqnwrm')))

        print('localizou text area')
        # reply_textarea.clear()
        # print('limpou text area') # Limpa o conteúdo existente no campo
        reply_textarea.send_keys(reply_text)
        reply_textarea.send_keys(Keys.RETURN)
        print('enviou comentario')

# Defina as informações necessárias
username = 'teste_bot2023'
password = 'teste1234'
post_link = 'Ct1bmVRumAD'
comment_text = ''

# Crie uma instância de ReplyBot
bot = ReplyBot()

# Inicialize o ReplyBot
bot.initialize_crawler(post_link=post_link, username=username, password=password, comment_text=comment_text)

# Adicione um loop infinito para manter o programa em execução
while True:
    # Aguarde uma entrada do usuário para decidir se o programa deve ser encerrado
    user_input = input("Digite 'sair' para encerrar o programa: ")
    if user_input.lower() == "sair":
        break  # Saia do loop se o usuário digitar 'sair'

