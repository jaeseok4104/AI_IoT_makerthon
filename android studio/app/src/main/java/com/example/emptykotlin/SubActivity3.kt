package com.example.emptykotlin

import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.github.mikephil.charting.components.AxisBase
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.ScatterData
import com.github.mikephil.charting.data.ScatterDataSet
import com.github.mikephil.charting.formatter.IAxisValueFormatter
import com.github.mikephil.charting.formatter.ValueFormatter
import com.github.mikephil.charting.utils.ColorTemplate
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_sub3.*
import org.json.JSONArray
import java.lang.Exception
import java.sql.Time
import java.time.Duration
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.temporal.ChronoUnit


class SubActivity3 : AppCompatActivity() {

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sub3)

        val sDataSet = ScatterDataSet(getData(), "Lab");
        val sData = ScatterData(sDataSet)
        sDataSet.colors = ColorTemplate.COLORFUL_COLORS.toList()
        SChart.data = sData

        try {
            setValue()
            sDataSet.valueFormatter = LValueFormatter()
        }catch (e:Exception){
            Sub3Txt.text = e.toString()
        }
        setSpinner()
        SChart.invalidate()
    }

    fun setSpinner(){
        YearSpinner?.onItemSelectedListener = object :AdapterView.OnItemSelectedListener{
            override fun onNothingSelected(p0: AdapterView<*>?) {
            }
            override fun onItemSelected(p0: AdapterView<*>?, p1: View?, p2: Int, p3: Long) {
                val str = YearSpinner.getItemAtPosition(p2).toString()
            }
        }

    }

    fun setValue(){
        val xA = SChart.xAxis
        val yA = SChart.axisLeft
        val sA = SChart.axisRight

        yA.axisMinimum=0f
        yA.axisMaximum=24f*60*60
        sA.axisMinimum=0f
        sA.axisMaximum=24f*60*60

        yA.setLabelCount(7,true)
        sA.setLabelCount(7,true)
        xA.position = XAxis.XAxisPosition.BOTTOM

        xA.valueFormatter = XValFormatter()
        yA.valueFormatter = LValueFormatter()
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun getData():ArrayList<Entry>{
        val TimeArr = ArrayList<LocalDateTime>()
        val YearList = ArrayList<String>()
        try {
            if (intent.hasExtra("JSONArr")) {
                val JArr = JSONArray(intent.getStringExtra("JSONArr"))
                for (i in 0 until JArr.length()-1) {
                    val JObj = JArr.getJSONObject(i)
                    val Temp = JObj.get("LastUpdate").toString()
                    val T = LocalDateTime.parse(Temp.substring(0, 10) + "T" + Temp.substring(11))
                    TimeArr.add(T)
                    var AddYear = true
                    val YStr = T.year.toString()
                    for(i in 0 until YearList.size){
                        if (YearList[i]==YStr){
                            AddYear = false
                            break
                        }
                    }
                    if (AddYear){YearList.add(YStr)}
                }
                YearSpinner.adapter = ArrayAdapter(this,android.R.layout.simple_spinner_dropdown_item,YearList.toArray())

                var sum = 0L               
                for (i in 0 until JArr.length()-1){
                    val JObj1 = JArr.getJSONObject(i)
                    val TD1 = JObj1.get("TextData").toString()

                    if (TD1 == "studyfinsh"||TD1=="sleep") {
                        val JObj2 = JArr.getJSONObject(i-1)
                        val TD2 = JObj2.get("TextData").toString()
                        if (TD2 == "studystart"||TD2 =="awake") {
                            val LU1 = JObj1.get("LastUpdate").toString()
                            val T1 = LocalDateTime.parse(LU1.substring(0, 10) + "T" + LU1.substring(11))
                            val LU2 = JObj2.get("LastUpdate").toString()
                            val T2 = LocalDateTime.parse(LU2.substring(0, 10) + "T" + LU2.substring(11))

                            sum += Duration.between(T2,T1).seconds
                        }
                    }
                }


                if (sum<60){
                    Sub3Txt.text = "총"+sum.toInt().toString()+"초 공부했습니다."
                }else if (sum>=60&&sum<60*60){
                    val sec = (sum%60).toInt()
                    val min = (sum/60).toInt()
                    Sub3Txt.text = String.format("총 %d분 %d초 공부했습니다.",sec,min)
                }else {
                    val sec = (sum%60).toInt()
                    val min = (sum/60%60).toInt()
                    val hour = (sum/60/60).toInt()
                    Sub3Txt.text = String.format("총 %d시간 %d분 %d초 공부했습니다.",hour,min,sec)
                }


            }
        }
        catch (e:Exception) {
            Sub3Txt.text = e.toString()
        }
        val entries = ArrayList<Entry>()
            for (i in 0 until TimeArr.size) {
                val T = TimeArr[i]
                val Sum = T.hour * 3600f + T.minute * 60f + T.second
                val D = T.dayOfYear
                entries.add(Entry(D.toFloat(), Sum))
            }
        return entries
    }

    inner class LValueFormatter():ValueFormatter(){
        override fun getPointLabel(entry: Entry?): String {
            try {
                var T= entry!!.y.toInt()
                val hh = T/3600
                val mm = T/60%60
                val ss = T%60
                return "$hh:$mm:$ss"
            }catch (e:Exception){
                Sub3Txt.text = e.toString()
                return ""
            }
        }

        override fun getFormattedValue(value: Float): String {
            return value.toString()
        }

        override fun getAxisLabel(value: Float, axis: AxisBase?): String {
            try {
                val T = value.toInt()
                val hh = T/3600
                val mm = T/60%60
                val ss = T%60
                return "$hh:$mm:$ss"
            }catch (e:Exception){
                Sub3Txt.text = e.toString()
                return ""
            }
        }
    }

    inner class XValFormatter():ValueFormatter(){
        override fun getFormattedValue(value: Float): String {
            return value.toString()
        }

        @RequiresApi(Build.VERSION_CODES.O)
        override fun getAxisLabel(value: Float, axis: AxisBase?): String {
            try {
                val D = value.toInt()
                val S = LocalDate.ofYearDay(2020,D).toString()
                return S.substring(5)
            }catch (e:Exception){
                Sub3Txt.text = e.toString()
                return ""
            }
        }
    }
}