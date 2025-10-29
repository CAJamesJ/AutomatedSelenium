from selenium import webdriver
import time
import os

def is_recording_enabled():
    try:
        with open("recording_flag.txt", "r") as f:
            return f.read().strip() == "True"
    except FileNotFoundError:
        return False

def inject_click_logger(driver):
    driver.execute_script("""
        if (window.__clickLoggerInjected) {
            document.removeEventListener('click', window.__clickLoggerHandler);
            window.__clickLoggerInjected = false;
        }

        window.__clickLoggerHandler = function(event) {
            const el = event.target;
            const id = el.id || '';
            let identifier = '';
            if (id) {
                identifier = 'ID: ' + id;
            } else {
                const parts = [];
                let element = el;
                while (element && element.nodeType === Node.ELEMENT_NODE) {
                    let index = 1;
                    let sibling = element.previousSibling;
                    while (sibling) {
                        if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === element.tagName) {
                            index++;
                        }
                        sibling = sibling.previousSibling;
                    }
                    const tagName = element.tagName.toLowerCase();
                    const part = tagName + '[' + index + ']';
                    parts.unshift(part);
                    element = element.parentNode;
                }
                const xpath = parts.length ? '/' + parts.join('/') : '';
                identifier = xpath ? 'XPath: ' + xpath : 'No ID or XPath';
            }

            fetch('http://localhost:5000/log', {
                method: 'POST',
                headers: {'Content-Type': 'text/plain'},
                body: identifier + '\\n'
            });
        };

        document.addEventListener('click', window.__clickLoggerHandler);
        window.__clickLoggerInjected = true;
    """)

# Setup Edge WebDriver
driver = webdriver.Edge()
driver.get("https://dev.sorrl.mcss.gov.on.ca/SORRL/public/login.xhtml")


try:
    recording_active = False
    while True:
        if is_recording_enabled():
            if not recording_active:
                inject_click_logger(driver)
                recording_active = True
        else:
            if recording_active:
                # Remove the click handler
                driver.execute_script("""
                    if (window.__clickLoggerInjected) {
                        document.removeEventListener('click', window.__clickLoggerHandler);
                        window.__clickLoggerInjected = false;
                    }
                """)
                recording_active = False
        time.sleep(0.5)
except KeyboardInterrupt:
    driver.quit()


# from selenium import webdriver
# from selenium.webdriver.edge.service import Service
# import time

# def inject_click_logger(driver):
#     driver.execute_script("""
#         if (!window.__clickLoggerInjected) {
#             window.__clickLoggerInjected = true;

#             function getXPath(element) {
#                 if (element.id) return '//*[@id=\"' + element.id + '\"]';
#                 const parts = [];
#                 while (element && element.nodeType === Node.ELEMENT_NODE) {
#                     let index = 1;
#                     let sibling = element.previousSibling;
#                     while (sibling) {
#                         if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === element.tagName) {
#                             index++;
#                         }
#                         sibling = sibling.previousSibling;
#                     }
#                     const tagName = element.tagName.toLowerCase();
#                     const part = tagName + '[' + index + ']';
#                     parts.unshift(part);
#                     element = element.parentNode;
#                 }
#                 return '/' + parts.join('/');
#             }

            
#         document.addEventListener('click', function(event) {
#             const el = event.target;
#             const tag = el.tagName;
#             const id = el.id || '';
#             const className = el.className || '';
#             const text = el.innerText || '';

#             function getXPath(element) {
#                 const parts = [];
#                 while (element && element.nodeType === Node.ELEMENT_NODE) {
#                     let index = 1;
#                     let sibling = element.previousSibling;
#                     while (sibling) {
#                         if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === element.tagName) {
#                             index++;
#                         }
#                         sibling = sibling.previousSibling;
#                     }
#                     const tagName = element.tagName.toLowerCase();
#                     const part = tagName + '[' + index + ']';
#                     parts.unshift(part);
#                     element = element.parentNode;
#                 }
#                 return parts.length ? '/' + parts.join('/') : '';
#             }

#             let identifier = '';
#             if (id) {
#                 identifier = 'ID: ' + id;
#             } else {
#                 const xpath = getXPath(el);
#                 identifier = xpath ? 'XPath: ' + xpath : 'No ID or XPath';
#             }

#             //const log = `${new Date().toISOString()} | <${tag}> | ${identifier} | Class: ${className} | Text: ${text}\\n`;
#             const log = `${identifier}\\n`;
#             fetch('http://localhost:5000/log', {
#                 method: 'POST',
#                 headers: {'Content-Type': 'text/plain'},
#                 body: log
#             });
#         });

#         }
#     """)

# # Setup Edge WebDriver
# driver = webdriver.Edge()
# driver.maximize_window()
# driver.get("https://google.com")  # You can change this or navigate freely

# # Initial injection
# inject_click_logger(driver)

# # Keep browser open and re-inject periodically
# try:
#     while True:
#         inject_click_logger(driver)
#         time.sleep(2)  # Re-inject every 2 seconds to catch new pages
# except KeyboardInterrupt:
#     driver.quit()