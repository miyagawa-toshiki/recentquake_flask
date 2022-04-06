function func1() {
    

    //var Date = Number(now.getDate());
    //var next_day = Date+1;
    //console.log(var)
    let next_day_button=document.getElementById('next_day');
    next_day_button.disabled=true;

    //ここのコードの理解
    var pdate=new Date().getDate();
    var ndate;
    ndate=new Date().getDate();
    if(pdate!=ndate) next_day_activate();
    pdate=ndate;
}

function next_day_activate() {
    let next_day_button=document.getElementById('next_day');
    next_day_button.disabled=false;
    let data_button = document.getElementById('button1');
    data_button.disabled=false;
}