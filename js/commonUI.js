(function () {
    var btn = document.createElement('button');
    btn.innerHTML = '清除图像';
    btn.style.cssText = `
        position:absolute;
        left: 10px;
        bottom: 10px;
        background: rgb(42, 64, 173);
        color: #fff;
        border: none;
        padding: 5px 10px;
        z-index: 1000000;
        cursor: pointer;
    `;

    var btntheme = document.createElement('button');
    btntheme.innerHTML = '主题切换';
    btntheme.style.cssText = `
        position:absolute;
        left: 100px;
        bottom: 10px;
        background: rgb(42, 64, 173);
        color: #fff;
        border: none;
        padding: 5px 10px;
        z-index: 1000000;
        cursor: pointer;
    `;

    var btncity = document.createElement('button');
    btncity.innerHTML = '城市切换';
    btncity.style.cssText = `
        position:absolute;
        left: 200px;
        bottom: 10px;
        background: rgb(42, 64, 173);
        color: #fff;
        border: none;
        padding: 5px 10px;
        z-index: 1000000;
        cursor: pointer;
    `;

    var btnchina = document.createElement('button');
    btnchina.innerHTML = '回到全国';
    btnchina.style.cssText = `
        position:absolute;
        left: 300px;
        bottom: 10px;
        background: rgb(42, 64, 173);
        color: #fff;
        border: none;
        padding: 5px 10px;
        z-index: 1000000;
        cursor: pointer;
    `;

    btn.onclick = function () {
        (typeof myChart !== 'undefined') && myChart.dispose();
        (typeof chart !== 'undefined') && chart.dispose();
    }

    var styles = [
                'mapbox://styles/nocmk2/cjkweod6234ad2rmvyzsqj8rp',
                'mapbox://styles/nocmk2/cjkuul5zo0tcj2rnx9zdfqnt1',
                'mapbox://styles/nocmk2/cjkv0dnpu0clc2rujllb4wgrz', // 卫星
                'mapbox://styles/nocmk2/cjkuv4wkp1q382sr9a0anszjw',   // 黑色
                'mapbox://styles/nocmk2/cjkwmeajh3bat2rkhx64r5tid', // 紫黑色
                'mapbox://styles/nocmk2/cjkwe249w34pt2rpa78g1gj9s', //紫白
                'mapbox://styles/nocmk2/cjkwip1zw3a1s2sqnz5ns5qo3',
                'mapbox://styles/nocmk2/cjkxcj15d0fou2so3dw4ckmgj',  // default blue
                'mapbox://styles/nocmk2/cjkxclu2241yp2sqnqo1pd12p',
    ]
    var s = 1;
    btntheme.onclick = function () {
            mapboxstyle = styles[Math.round(Math.random()*9)-1] // 黑色
            console.log('change style to:' + mapboxstyle)
            myChart.setOption({mapbox3D: {
                style: mapboxstyle
            }
        });
    }

    btncity.onclick = function () {
        flyToNextCity()
    }

    btnchina.onclick = function () {
        backtochina()
    }

    document.body.appendChild(btn);
    document.body.appendChild(btntheme);
    document.body.appendChild(btncity);
    document.body.appendChild(btnchina);
})();