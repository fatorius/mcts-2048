from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains, Keys

from game import Game
from mcts import MCTS

driver = webdriver.Safari()
driver.get("https://fatorius.github.io/2048/")

while True:
    page_html = BeautifulSoup(driver.page_source, features="html.parser")
    state = []

    for element in page_html.find_all("div", class_="cell"):
        if element.text == "":
            state.append(0)
            continue

        state.append(int(element.text))

    game = Game()
    game.set_state(state)
    mcts = MCTS(iterations=10000)
    result = mcts.search(game)

    if result['action'] == "down":
        ActionChains(driver).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()
    elif result['action'] == "up":
        ActionChains(driver).key_down(Keys.ARROW_UP).key_up(Keys.ARROW_UP).perform()
    elif result['action'] == "left":
        ActionChains(driver).key_down(Keys.ARROW_LEFT).key_up(Keys.ARROW_LEFT).perform()
    else:
        ActionChains(driver).key_down(Keys.ARROW_RIGHT).key_up(Keys.ARROW_RIGHT).perform()
