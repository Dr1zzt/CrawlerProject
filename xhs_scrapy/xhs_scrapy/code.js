const {DES_encrypt} = require('./source.js');
function myatob(data) {
    const keystr =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    function atobLookup(chr) {
        const index = keystr.indexOf(chr);
        return index < 0 ? undefined : index;
    }

    data = data.replace(/[ \t\n\f\r]/g, "");

    if (data.length % 4 === 0) {
        data = data.replace(/==?$/, "");
    }

    if (data.length % 4 === 1 || /[^+/0-9A-Za-z]/.test(data)) {
        return null;
    }
    let output = "";
    let buffer = 0;
    let accumulatedBits = 0;

    for (let i = 0; i < data.length; i++) {

        buffer <<= 6;
        buffer |= atobLookup(data[i]);
        accumulatedBits += 6;
        if (accumulatedBits === 24) {
            output += String.fromCharCode((buffer & 0xff0000) >> 16);
            output += String.fromCharCode((buffer & 0xff00) >> 8);
            output += String.fromCharCode(buffer & 0xff);
            buffer = accumulatedBits = 0;
        }
    }

    if (accumulatedBits === 12) {
        buffer >>= 4;
        output += String.fromCharCode(buffer);
    } else if (accumulatedBits === 18) {
        buffer >>= 2;
        output += String.fromCharCode((buffer & 0xff00) >> 8);
        output += String.fromCharCode(buffer & 0xff);
    }
    return output;
}

function mybtoa(s) {
    const keystr =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    function btoaLookup(index) {
        if (index >= 0 && index < 64) {
            return keystr[index];
        }
        return undefined;
    }

    let i;
    for (i = 0; i < s.length; i++) {
        if (s.charCodeAt(i) > 255) {
            return null;
        }
    }
    let out = "";
    for (i = 0; i < s.length; i += 3) {
        const groupsOfSix = [undefined, undefined, undefined, undefined];
        groupsOfSix[0] = s.charCodeAt(i) >> 2;
        groupsOfSix[1] = (s.charCodeAt(i) & 0x03) << 4;
        if (s.length > i + 1) {
            groupsOfSix[1] |= s.charCodeAt(i + 1) >> 4;
            groupsOfSix[2] = (s.charCodeAt(i + 1) & 0x0f) << 2;
        }
        if (s.length > i + 2) {
            groupsOfSix[2] |= s.charCodeAt(i + 2) >> 6;
            groupsOfSix[3] = s.charCodeAt(i + 2) & 0x3f;
        }
        for (let j = 0; j < groupsOfSix.length; j++) {
            if (typeof groupsOfSix[j] === "undefined") {
                out += "=";
            } else {
                out += btoaLookup(groupsOfSix[j]);
            }
        }
    }
    return out;
}



//随机数函数
function RandomNum(minNum, maxNum) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * minNum + 1, 10);
            break;
        case 2:
            return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
            break;
        default:
            return 0;
            break;
    }
}

//小程序
function get_sli(distance, k,slide_info) {
    var _0x1e6365 = slide_info[0];

    var encrypt_key = DES_encrypt("sshummei", myatob(k), 0, 8);
    var data = {
        "d":distance/372,
        "m": _0x1e6365,
        "c": slide_info[1]+RandomNum(10, 50),
        // "m":[[0.7,0,1],[11.7,0,101],[21.7,0,202]],
        // "c":226,
        "w": 372,
        "h": 186,
        "os": "weapp",
        "cs": 0,
        "wd": 0,
        "sm": 1
    }
    console.log(JSON.stringify(data))
    return mybtoa(DES_encrypt(encrypt_key, JSON.stringify(data), 1, 0))
}

//console.log(myatob("+3gzE2jUtyM="))
var kk = DES_encrypt("sshummei", myatob("+3gzE2jUtyM="), 0, 8);
console.log(DES_encrypt(kk, myatob('4R/HcRQBmcxue7lIg3i4nfy/hFjxIKJi+rr5gwiFLwBEauCd8WgJbxJZ5lznAPpspRnUN2+/7VSAnHq62i3LC7+ozyEbs1dIrbm6+RZxEWMoPp1fyE4ImChavtyAFBvOwOlkYI2oC/jLIzTDyXsJgm05cWrDIuvMoDva5R8AcZsESLRg6xvwCrS5cIBNsC7neiKeLkIjJ6vW5Skmtj3g090AWmOnHQRxN5+a1HNSXKlcG7M7QDiXv5NxpNgdZ3epnki+m5yNlV1WPnX02ttWtpe1PDEA3pifro8w/9CFDv+Gi9i3U85yfkXqOwCbACjtJU0IPghZiilSDmU8bBepXiF5CyQSqE80Cku3fc3jzSs4zqwrKjMEU0ZltgMI4eepczRFE7/zppV0X/bVnTuxCB2xaoDyd4xv0ZjBTuIPu7lUbKfJQeKcYt8PLdpLyamR5UmydmJx7ErJ4PQF3XbvxnIWyyk85eMHafZf1s1woF9bcWZomPYivTzoGAivI29lklZNWMYhncbejlt2Ao9OxpNqz3kyFOo9PYGWWY1K3lXu47WcIgWlHx/n+xFsY+pBagwOy+nDqWg/BOoGFSmzAJWDR/nPaIQ6mvYQHJLnhXEnzOBi709dcZUCrzn6rVQb5eZEluINXBQOz1vJZpIA7QnOb/P8cSclhTTJedov1OY4L//9RF7ssAItmVUjAyCpo48iUVqXZv1ZnmQci//CDu+5M9TMCEMw8O2MYXMZkzbKAZl32yZM4m7L5LuXgqph95whfQjo4RjylkmuJaoIjv7/RenvAuK+jn7ApZLTtJSmZNVcNEc1LwFKvPgrDGLOf9fG/COA6CXYT0xSD2vxz8HQAyXDPrjhwHssSDq4jvJjvgH4FT77UhJ/LtN6ehowOrcf7B11tBxoJ9PlX5ajeWLXfiLVAiWE/zgkGr/t7sirb27VNhOyEZU1kTeu8by2O8gLDP6TtIWlUKL73+HiUy/82Uk37Xfkp6XG33rK+hno2iJYoMp6INwpm7Aybgdng6C7Sw8KjAcm43P23T+znz3s1zqfrqWpHUXCz7B6mI7XK+rkRmroqvdTLaSLBycE/xfCxIly/OYJTLWt//jw8vEp0KAnjBhnNacdHkss3LkjNPuXvATnUy8lvCIBFq3OoG0B+JW/LCYbPbAR6Li+TQoe5DbnZ3vVfDeRHz562u9Cra9E7cFGnBnSEjxkQqpEZKTT9AvOQHuSMa4ecS3a92dVPOmT25NsP+FKM257lekIKioeHuOcifhSercF3A4zK2feK90jE6ahAgD8bfSzHbxpbYhz+B2LDQLjhH7Loq6meHxtaVHpnentwkJ0GdFmc/Ep6xEtaorD809DM7sRpXV3zxlMCGtbY3FbECEbptyJNwk3pHhE+eF3gN8gYOtl0t2G2rjjh3YqG6/n/UnL5sIBREDxq72XLBBiImUmvDgXF/tQiOCm8aqmpyTNBjyWfQkDi75nX6KW4R/hkFLB2PDfm8ddbzGkTupvWaTAl4jEaynSFSWtP+aLTTXPVllSbIUhpTM0Y3RMmhlkj6qAmFe6RrXbJUe2XotoiVWMqniKU56o4gNZnWStN9pe9YvtRI+FRaFhRCZpJ2zGSlRxh+rNK5DqxQHa+CbLHVvbcIMkrMizfiugtYKbLUzGZFZdXhtEyrNa01sG03T1K9RYtasDb80fwRBhJCtfg7pVEL1TRpL7etwI/MCdwFSNNM8KfoBH70UsYVwQWjwCZdEh1jB+hbP063O7rOwMygnumLg='), 0, 0))







