package com.example.emptykotlin

import android.content.Context
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.github.mikephil.charting.charts.BarChart
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter
import kotlinx.android.synthetic.main.activity_sub1.*
import org.json.JSONArray
import java.time.Duration
import java.time.LocalDateTime

class SubActivity1 : AppCompatActivity(){

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sub1)

        val TimeArr = ArrayList<LocalDateTime>()

        if(intent.hasExtra("JSONArr")){
            val JArr = JSONArray(intent.getStringExtra("JSONArr"))
            for(i in 0 until JArr.length()){
                val JObj = JArr.getJSONObject(i)
                val Temp = JObj.get("LastTime").toString()
                val T = Temp.substring(0,10)+"T"+Temp.substring(11)
                TimeArr.add(LocalDateTime.parse(T))
            }
        }
        else{
            TimeArr.add(LocalDateTime.now())
            TimeArr.add(TimeArr[0].plusSeconds(70))
            TimeArr.add(TimeArr[0].plusSeconds(110))
            TimeArr.add(TimeArr[0].plusSeconds(150))
            TimeArr.add(TimeArr[0].plusSeconds(180))
            if (intent.hasExtra("test")){
                TimeArr.add(TimeArr[0].plusSeconds(240))
            }
        }
        cal(TimeArr)


        //example data
        //example()
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun example(){

        val dataArr1 = arrayListOf(3f,5f,8f,13f)
        val dataArr2 = arrayListOf(3f,6f,9f,12f)

        val entries1 = ArrayList<BarEntry>()
        val entries2 = ArrayList<BarEntry>()

        for (i in 0 until dataArr1.size){
            entries1.add(BarEntry(i.toFloat(), dataArr1[i]))
            entries2.add(BarEntry(i.toFloat(), dataArr2[i]))

        }
        val set1 = BarDataSet(entries1,"A")
        val set2 = BarDataSet(entries2,"B")

        val groupSpace_ = 0.06f
        val barSpace_ = 0.02f
        val barWidth_ = 0.45f

        val bData = BarData(set1, set2)
        bData.barWidth = barWidth_
        BarChart1.data = bData
        BarChart1.groupBars(-0.5f,groupSpace_,barSpace_)
        BarChart1.setDrawGridBackground(false)

//      XAxisToString(dataArr[0].T.toLocalDate().toString())
        BarChart1.invalidate()
    }


    @RequiresApi(Build.VERSION_CODES.O)
    fun cal(dataArr:ArrayList<LocalDateTime>)
    {
        var studyT = 0
        var sleepT = 0

        for(i in 2 until dataArr.size step 2) {
            val T = Duration.between(dataArr[i-1], dataArr[i]).seconds.toInt()
            sleepT += T
        }
        for(i in 0 until dataArr.size step 2) {
            val T = Duration.between(dataArr[i], dataArr[i+1]).seconds.toInt()
            studyT += T
        }

        val fullT = studyT + sleepT
        val entries1 = ArrayList<BarEntry>()
        val entries2 = ArrayList<BarEntry>()

        entries1.add(BarEntry(1f,fullT.toFloat()))
        entries2.add(BarEntry(1f,sleepT.toFloat()))
        val set1 = BarDataSet(entries1,"FullTime")
        val set2 = BarDataSet(entries2, "SleepTime")

        val groupSpace_ = 0.06f
        val barSpace_ = 0.02f
        val barWidth_ = 0.20f

        set1.color = Color.RED
        set2.color = Color.BLACK
        val bData = BarData(set1, set2)
        bData.barWidth = barWidth_
        BarChart1.data = bData
        BarChart1.groupBars(0.5f,groupSpace_,barSpace_)
        BarChart1.setDrawGridBackground(false)

        XAxisToString(dataArr[0].toLocalDate().toString())
        BarChart1.invalidate()
    }

    fun XAxisToString(s:String){
        val xAxis_ = BarChart1.xAxis
        xAxis_.position = XAxis.XAxisPosition.BOTTOM
        xAxis_.setDrawGridLines(false)

        val label = ArrayList<String>()
        label.add(s)
        xAxis_.valueFormatter = IndexAxisValueFormatter(label)
    }
}