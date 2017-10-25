// ==UserScript==
// @name SMWC Preview
// @description Adds preview support to SMWC. You also need to install the native application in "userscript mode"
// @author randomdude999
// @match https://www.smwcentral.net/*
// ==/UserScript==

(function(){
    var searchParams = new URL(window.location).searchParams;

    function addLink(text, type, section, secondary_id_grabber) {
        if(document.querySelector("td > a[href^='/?p=section&s="+section+"']") !== null) {
            var link = document.createElement('a');
            var secondary_id;
            link.innerHTML = text;
            link.href = "x-smwc-preview:"+type+","+searchParams.get("id")
            if(typeof secondary_id_grabber !== "undefined") {
                link.href += ","+secondary_id_grabber();
            }
            var small = document.querySelectorAll("td > a[href*='dl.smwcentral.net/']")[1].parentElement.children[2];
            small.appendChild(document.createElement('br'));
            small.appendChild(link);
        }
    }

    if(searchParams.get("p") === "section"
            && searchParams.get("a") === "details"
            && searchParams.get("id") !== null) {
        // this is a details page
        addLink("Preview", "music", "smwmusic");
        addLink("Preview", "music", "brrsamples"); // most brr samples include preview spcs
        addLink("Play", "smwhack", "smwhacks");
        addLink("Play", "yihack", "yihacks");
        addLink("Play", "sram", "sramdatabase", () => {
            var hackURL = new URL(document.querySelector("td > a[href*='/?p=section&a=details']").href);
            return hackURL.searchParams.get("id");
        });
    }
})();