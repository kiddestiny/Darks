(function () {
    var btncity = document.createElement('button');
    btncity.innerHTML = '城市切换';
    btncity.style.cssText = `
        position:absolute;
        left: 0px;
        bottom: 0px;
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
        left: 0px;
        bottom: 30px;
        background: rgb(42, 64, 173);
        color: #fff;
        border: none;
        padding: 5px 10px;
        z-index: 1000000;
        cursor: pointer;
    `;

    var btntogglehis = document.createElement('button');
    btntogglehis.innerHTML = '历史数据';
    btntogglehis.style.cssText = `
        position:absolute;
        left: 0px;
        bottom: 60px;
        background: rgb(42, 64, 173);
        color: #fff;
        border: none;
        padding: 5px 10px;
        z-index: 1000000;
        cursor: pointer;
    `;

    btncity.onclick = function () {
        flyToNextCity()
    }

    btnchina.onclick = function () {
        backtochina()
    }

    hisdata = []
    btntogglehis.onclick = function () {
            console.log(hisdata)
            if(hisdata.length==0){       
                hisdata = option.series[1].data
                option.series[1].data = []
                console.log('123123')
             }else{
                option.series[1].data = hisdata
                hisdata = []
             }
             console.log(option)
                myChart.setOption(option,{
                    notMerge:false,
                    lazyUpdate:true,
                    silent:true
                });
    }

    document.body.appendChild(btncity);
    document.body.appendChild(btnchina);
    document.body.appendChild(btntogglehis);
})();