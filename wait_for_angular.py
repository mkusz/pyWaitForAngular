# coding=utf-8
"""
.. codeauthor:: Maciej 'maQ' Kusz
"""

from selenium.common.exceptions import TimeoutException

WAIT_FOR_ANGULAR_TIMEOUT = 10


class WaitForAngular(object):
    """ Helper class used for detect if all angular scripts has been fully processed
    so we are able to determine if whole page has been fully loaded. Object is created
    just to be able to use it with Selenium WebDriverWait
    """

    def __call__(self, driver):
        """ When object is called this function inject javascript code to the web page and
        execute it. When code is not executed in give point of time it raise an Exception and
        function returns False. If injected code was executed it means that angular was fully
        processed and functions returns True.
        Based on protractor code:
        https://github.com/angular/protractor/blob/c94f678cfbe142dcb88ef13610d850d60b5e1ccc/lib/clientsidescripts.js

        :param driver: webdriver instance
        :return: True if angular was fully processed, False otherwise
        """
        try:
            script = """
            var callback = arguments[arguments.length - 1];
            var el = document.querySelector('html');  //Selector of an element with ng-app
            if (!window.angular) {
                callback('false')
            }
            if (angular.getTestability) {
                angular.getTestability(el).whenStable(function(){callback('true')});
            } else {
                if (!angular.element(el).injector()) {
                    callback('false')
                }
                var browser = angular.element(el).injector().get('$browser');
                browser.notifyWhenNoOutstandingRequests(function(){callback('true')});
            }
            """
            driver.set_script_timeout(WAIT_FOR_ANGULAR_TIMEOUT)
            return driver.execute_async_script(script)
        except TimeoutException:
            return False
