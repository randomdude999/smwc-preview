// You can't send native messages from content scripts so this is just a relay of sorts
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        chrome.runtime.sendNativeMessage("randomdude999.smwc_preview", request);
});