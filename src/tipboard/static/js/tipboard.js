
// Definition of the Exception UnknownRenderer
var UnknownRenderer = function (rendererName) {
    this.name = "UnknownRederer";
    this.message = "Renderer: '" + rendererName + "' not found";
};
window.Tipboard = {};
UnknownRenderer.prototype = new Error();
UnknownRenderer.prototype.constructor = UnknownRenderer;

// Define UnknownUpdateFunction exceptions definition
var UnknownUpdateFunction = function (tileType) {
    this.name = "UnknownUpdateFunction";
    this.message = "Couldn't find update function for: " + tileType;
};
UnknownUpdateFunction.prototype = new Error();

function getFlipTime(node) {
    var classStr = $(node).attr("class");
    // TODO: make this flip time CUSTOM
    var flipTime = 4200;
    $.each(classStr.split(" "), function (idx, val) {
        var groups = /flip-time-(\d+)/.exec(val);
        if (Boolean(groups) && groups.length > 1) {
            flipTime = groups[1];
            flipTime = parseInt(flipTime, 10) * 1000;
            return false;
        }
    });
    return flipTime;
}


/**
 *
 * @returns WebSocketManager
 */
function initWebsocketManager() {
    return {

        onClose: function () {
            console.log("Web socket closed. Restarting...");
            setTimeout(Tipboard.WebSocketManager.init.bind(this), 1000);
        },

        onMessage: function (evt) {
            var tileData = JSON.parse(evt.data);
            if (tileData == null) {
                console.log("Web socket received NULL data");
            } else {
                console.log("Web socket received data: ", tileData);
                var tileId = Tipboard.Dashboard.escapeId(tileData.id);
                Tipboard.Dashboard.updateTile(
                    tileId,
                    tileData.tile_template,
                    tileData.data,
                    tileData.meta,
                    tileData.modified);
                }
        },

        onError: function (evt) {
            console.log("WebSocket error: " + evt.data);
        },

        init: function () {
            console.log("Initializing a new Web socket manager.");

            var protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

            var websocket = new WebSocket(protocol + window.location.host + "/communication/websocket");
            websocket.onopen = function (evt) {
                websocket.send("first_connection:" + window.location.pathname);
                console.log("Websocket: " + "first_connection:" + window.location.href)
            };
            websocket.onclose = function (evt) {
                Tipboard.WebSocketManager.onClose(evt);
            };
            websocket.onmessage = function (evt) {
                Tipboard.WebSocketManager.onMessage(evt);
            };
            websocket.onerror = function (evt) {
                Tipboard.WebSocketManager.onError(evt);
            };
        }
    };
}


function initTilesFliping() {
    // flipping tiles
    var flipContainers = $('div[id*="flip-time-"]');
    $.each(flipContainers, function (idx, flippingContainer) {
        Tipboard.Dashboard.autoAddFlipClasses(flippingContainer);
        var flipInterval = getFlipTime(flippingContainer);
        var flipIntervalId = setInterval(function () {
            var nextFlipIdx;
            var containerFlips = $(flippingContainer).find('.flippable');
            $(containerFlips).each(function (index, tile) {
                if ($(tile).hasClass("flippedforward")) {
                    nextFlipIdx = (index + 1) % containerFlips.length;
                    $(tile).removeClass("flippedforward");
                    return false; // break
                }
            });
            if (typeof (nextFlipIdx) !== 'undefined') {
                var tileToFlip = containerFlips[nextFlipIdx];
                $(tileToFlip).addClass("flippedforward");
            }
        }, flipInterval);
        Tipboard.Dashboard.flipIds.push(flipIntervalId);
    });
}


function initTiles() {
    initTilesFliping();
    $.each($("body > div"), function (rowIdx, row) {
        // show tiles number (like: 1/3)
        $.each($(row).children('div'), function (colIdx, col) {
            Tipboard.Dashboard.addTilesCounter(col);
        });
    });
}

var addEvent = function(object, type, callback) {
    if (object == null || typeof(object) == 'undefined') return;
    if (object.addEventListener) {
        object.addEventListener(type, callback, false);
    } else if (object.attachEvent) {
        object.attachEvent("on" + type, callback);
    } else {
        object["on"+type] = callback;
    }
};

const getTitleForChartJSTitle = function (data) {
    return (!('title' in data) || !('text' in data['title'])) ?
        { // When no title present
            display: false,
        } :
        {
            display: true,
            text: data['title']['text'],
            borderColor: ('borderColor' in data) ? data['borderColor'] : 'rgba(255, 255, 255, 1)',
            color: ('color' in data) ? data['color'] : ''
        };
};

/**
 *  Main function of tipboard.js
 *  Define the Palette object used for custom color
 *  Define the WebsocketClient connection (how to update tile by websocket)
 *  Define the Dashboard object behavior (flip time, register tiles func, etc)
 *  Define the $(document).ready(function()
 */
(function ($) {
    'use strict';

    addEvent(window, "resize", function(event) {
      location.href = location.href; // location.reload(); is not working on firefox...
    });
    Tipboard.Dashboard = {
        wsSocketTimeout: 900000,
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
    };
    Tipboard.Dashboard.UnknownUpdateFunction = UnknownUpdateFunction;
    Tipboard.WebSocketManager = initWebsocketManager();
    initDashboard(Tipboard);
    Chart.defaults.global.defaultFontColor = 'rgba(255, 255, 255, 0.83)';
    $(document).ready(function () {
        console.log('Tipboard starting');
        //TODO: resize event
        Tipboard.WebSocketManager.init();
        setInterval(Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager), Tipboard.Dashboard.wsSocketTimeout);
        initTiles()
    });
}($));

