(function(){
    var searchParams = new URL(window.location).searchParams;

    function addLink(text, type, section, custom_onclick) {
        if(document.querySelector("td > a[href^='/?p=section&s="+section+"']") !== null) {
            var link = document.createElement('a');
            link.innerHTML = text;
            if(typeof custom_onclick !== "undefined") {
                link.onclick = custom_onclick;
            } else {
                link.onclick = () => {
                    chrome.runtime.sendMessage({"type":type,"id":searchParams.get("id")});
                    return false;
                }
            }
            link.href = "#";
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
            var hackSearchP = new URL(document.querySelector("td > a[href*='/?p=section&a=details']").href).searchParams;
            chrome.runtime.sendMessage({"type":"sram","id":searchParams.get("id"),"secondary_id":hackSearchP.get("id")});
            return false;
        });
    }
})();