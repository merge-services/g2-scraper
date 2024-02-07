import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

BY = uc.By
import pandas as pd
from playsound import playsound
import random
import pyautogui as mouse
import re
import os

### Cloudflare bypass

# driver.execute_script('''window.open("https://www.g2.com/products/selenium-webdriver/reviews","_blank");''') # open page in new tab
# time.sleep(5) # wait until page has loaded
# driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
# driver.close() # close first tab
# driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab
# time.sleep(2)
# driver.get("https://google.com")
# time.sleep(2)
review_titles = []
liked = []
disliked = []
problems_solved = []
stars = []
reviewer_names = []
reviewer_jobs = []
reviewer_company = []
review_dates = []
companies = {
    'cloudtalk': 500,
}

for comp in companies.keys():
    COMPANY = comp
    pages = int(companies[comp] / 25) + 1

    for i in range(pages):
        chrome_options = Options()
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
        driver = uc.Chrome(use_subprocess=True, headless=False, options=chrome_options)
        url = f"https://www.g2.com/products/{COMPANY}/reviews"
        if i == 0:
            driver.execute_script(
                f'window.open("{url}","_blank");'
            )  # open page in new tab
        else:
            driver.execute_script(
                f'window.open("{url}?page=4","_blank");'
            )  # open page in new tab
        time.sleep(4)
        print("clicking")
        mouse.click()
        time.sleep(2)  # wait until page has loaded

        driver.switch_to.window(window_name=driver.window_handles[0])  # switch to first tab
        driver.close()  # close first tab
        driver.switch_to.window(
            window_name=driver.window_handles[0]
        )  # switch back to new tab
        time.sleep(1)
        driver.get("https://google.com")
        time.sleep(1)

        if i == 0:
            driver.get(f"https://www.g2.com/products/{COMPANY}/reviews")
        else:
            driver.get(
                f"https://www.g2.com/products/{COMPANY}/reviews?page={i}"
            )  # this should pass cloudflare captchas now

        # driver.switch_to.window(window_name=driver.window_handles[1] )
        time.sleep(3)

        reviews = driver.find_elements(BY.CSS_SELECTOR, "div.paper")
        print(len(reviews))

        ### init reviews

        for review in reviews:
            try:
                title = review.find_element(BY.CSS_SELECTOR, "div.m-0.l2")
                review_titles.append(title.get_attribute("innerHTML"))
                try:
                    review_body_parts = review.find_elements(
                        BY.CLASS_NAME, "formatted-text"
                    )
                except:
                    liked.append("no liked")
                    disliked.append("no disliked")
                    problems_solved.append("no problems solved")

                try:
                    liked.append(review_body_parts[0].get_attribute("innerHTML"))
                except:
                    liked.append("no liked")
                try:
                    disliked.append(review_body_parts[1].get_attribute("innerHTML"))
                except:
                    disliked.append("no disliked")
                try:
                    problems_solved.append(review_body_parts[2].get_attribute("innerHTML"))
                except:
                    problems_solved.append("no problems solved")

                try:
                    star = review.find_element(BY.CSS_SELECTOR, "div.stars")
                    rating = star.get_attribute("class")
                    match = re.search(r"\bstars-(\d+)\b", rating)
                    if match:
                        # Extracted number
                        number = match.group(1)
                        stars.append(number)
                    else:
                        stars.append("no stars")
                except:
                    stars.append("no stars")

                try:
                    review_date = review.find_element(
                        BY.CSS_SELECTOR, "span.x-current-review-date"
                    )
                    date = review_date.get_attribute("innerHTML")
                    meta_date_match = re.search(
                        r'<meta content="([^"]+)" itemprop="datePublished">', date
                    )
                    if meta_date_match:
                        extracted_meta_date = meta_date_match.group(1)
                    review_dates.append(extracted_meta_date)
                except:
                    review_dates.append("no date")

                try:
                    reviewer_name = review.find_element(
                        BY.CSS_SELECTOR, 'meta[itemprop="name"]'
                    )
                    reviewer_names.append(reviewer_name.get_attribute("content"))
                except:
                    reviewer_names.append("no name")

                try:
                    reviewer_job = review.find_element(BY.CSS_SELECTOR, "div.mt-4th")
                    reviewer_job = reviewer_job.get_attribute("innerHTML")
                    reviewer_jobs.append(reviewer_job)
                except:
                    reviewer_jobs.append("no job")

            except:
                print("no title")

            # Let the user actually see something!

            # reviews = driver.find_elements_by_css_selector("id^=survey-response-")

            # turning array to df
        os.system('kill.bat ' + str(driver.browser_pid))
        driver.quit()

    df = pd.DataFrame(
        {
            "review_titles": review_titles,
            "liked": liked,
            "disliked": disliked,
            "problems_solved": problems_solved,
            "stars": stars,
            "review_date": review_dates,
            "reviewer_name": reviewer_names,
            "reviewer_job": reviewer_jobs,
        }
    )

    df.to_csv(COMPANY + ".csv", encoding="utf-8")
    print("done")




exit()
