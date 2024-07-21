window.onload = function () {
    //获取日期 输入框
    var oInput = document.getElementById('Dateinput');
    //获取日历
    var oCalender = document.getElementById('calender');
    //获取当前日期
    var oDate = new Date();
    //获取当年 年
    var year = oDate.getFullYear();
    //获取当前 月
    var month = oDate.getMonth() + 1;

    //日历框不能重复创建
    var flag = false;
    //日期输入框 获取焦点时 加载日历
    oInput.onfocus = function () {
        showDate(year, month);
    }

    //显示日历
    function showDate(year, month) {
        if (false == flag) {
            //1.日历标题
            var oTitle = document.createElement('div');
            oTitle.className = 'title';

            //1.1日历标题文本
            var prevM = 0;
            var nextM = 0;

            prevM = month - 1;
            nextM = month + 1;

            //当月份为1时 上一个月为12
            if (month == 1) {
                prevM = 12;
            }//当月份为12时 下一个月为1
            else if (month == 12) {
                nextM = 1;
            }

            var titleHtml = "";
            titleHtml += '<div class="prev" id="prev"><span>';
            titleHtml += prevM + '</span>月</div>';
            titleHtml += '<div class="now">';
            titleHtml += '<span class="span">';
            titleHtml += year;
            titleHtml += '</span>年';
            titleHtml += '<span class="span">' + month;
            titleHtml += '</span>月</div>';
            titleHtml += '<div class="next" id="next"><span>';
            titleHtml += nextM + '</span>月</div>';

            oTitle.innerHTML = titleHtml;
            //将日历标题 拼接到日历
            oCalender.appendChild(oTitle);

            //1.2获取日历 表头元素（以便添加事件）
            var oSpans = oCalender.getElementsByTagName('span');
            var prevMonth = oSpans[0];
            var nextMonth = oSpans[3];
            var nowMonth = oSpans[2];
            var nowYear = oSpans[1];

            //2.创建星期 表头
            var otable = document.createElement('table');
            var othead = document.createElement('thead');
            var otr = document.createElement('tr');

            //2.1表头内容填充
            var arr = ['日', '一', '二', '三', '四', '五', '六'];
            for (var i = 0; i < arr.length; i++) {
                //创建th
                var oth = document.createElement('th');
                oth.innerHTML = arr[i];
                otr.appendChild(oth);
            }

            //2.2将表头加入到日历
            othead.appendChild(otr);
            otable.appendChild(othead);
            oCalender.appendChild(otable);

            //3.添加 当前日历 全部日期
            //3.1.先获得当期月 有多少天
            var dayNum = 0;
            if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
                dayNum = 31;
            } else if (month == 4 || month == 6 || month == 9 || month == 11) {
                dayNum = 30;
            } else if (month == 2 && isLeapYear(year)) {
                dayNum = 29;
            } else {
                dayNum = 28;
            }

            //3.2.创建 6行7列 日期容器
            var otbody = document.createElement('tbody');
            for (var i = 0; i < 6; i++) {
                var otr = document.createElement('tr');
                for (var j = 0; j < 7; j++) {
                    var otd = document.createElement('td');
                    otr.appendChild(otd);
                }
                otbody.appendChild(otr);
            }
            otable.appendChild(otbody);

            //3.3获得 1号对应的是星期几
            //3.3.1.将当月1号赋值给日期变量
            oDate.setFullYear(year);
            //注意 js日期的月份是从0 开始计算
            oDate.setMonth(month - 1);
            oDate.setDate(1);

            //3.3.2.计算1号在第一行日期容器中的位置，依次给日期容器填充内容
            //注意 js中 getDay方法是获取当前日期是星期几
            var week = oDate.getDay();
            var otds = oCalender.getElementsByTagName('td');
            for (var i = 0; i < dayNum; i++) {
                otds[i + week].innerHTML = i + 1;
            }


            //让当前日期显示红色、后面的显示蓝色
            showColor(otds);
            //给左右月份绑定点击事件
            monthEvent();
            //判断最后一行是否全为空
            lastTr(otds);
            flag = true;
            document.getElementById('calender').style.display = "block";
        }
    }

    //判断是否是闰年
    function isLeapYear(year) {
        if (year % 100 == 0 && year % 400 == 0) {
            return true;
        } else if (year % 100 != 0 && year % 4 == 0) {
            return true;
        } else {
            return false;
        }
    }

    //判断日期容器最后一行是否有值
    function lastTr(otds) {
        var flag = true;
        for (var i = 35; i < 42; i++) {
            if (otds[i].innerHTML != '') {
                flag = false;
            }
        }
        //全是空的
        if (flag) {
            for (var i = 35; i < 42; i++) {
                otds[i].style.display = 'none';
            }
        }
    }

    //当前日期显示红色、前面的显示灰色
    function showColor(otds) {
        //当前日期
        var nowday = new Date().getDate();
        var nowyear = new Date().getFullYear();
        var nowmonth = new Date().getMonth();

        var oCalendar = document.getElementById("calender");
        ospans = oCalendar.getElementsByTagName('span');
        var contralYear = ospans[1].innerHTML;
        var contralMonth = ospans[2].innerHTML;

        var oindex = 0;
        for (var i = 0; i < otds.length; i++) {
            if (nowday == otds[i].innerHTML && nowyear == contralYear && nowmonth + 1 == contralMonth) {
                otds[i].className = 'red';
                oindex = i;
            }
        }
    }

    //给左右月份绑定点击事件
    function monthEvent() {
        var oCalendar = document.getElementById("calender");
        var prevDiv = document.getElementById("prev");
        var nextDiv = document.getElementById("next");

        var prevMonth = prevDiv.getElementsByTagName("span");
        var nextMonth = nextDiv.getElementsByTagName("span");

        prevDiv.onclick = function () {
            flag = false;
            oCalendar.innerHTML = '';
            showDate(year, parseInt(prevMonth[0].innerHTML));
        }

        nextDiv.onclick = function () {
            flag = false;
            oCalendar.innerHTML = '';
            showDate(year, parseInt(nextMonth[0].innerHTML));
        }

    }
}