package com.example.emptykotlin

import android.graphics.Color
import android.os.Build
import android.os.Bundle
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.github.mikephil.charting.charts.LineChart
import java.time.LocalDateTime
import kotlinx.android.synthetic.main.activity_sub2.*
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.components.YAxis
import com.github.mikephil.charting.data.*
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet


class SubActivity2 : AppCompatActivity() {
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sub2)
        setChart()
    }

    fun setChart(){
        val dataArr1 = arrayListOf(3f,5f,8f,13f)
        val dataArr2 = arrayListOf(3f,6f,9f,12f)

        val entries1 = ArrayList<Entry>()
        val entries2 = ArrayList<Entry>()
        for (i in 0 until dataArr1.size){
            entries1.add(Entry(i.toFloat(), dataArr1[i]))
        }
        for (i in 0 until dataArr2.size){
            entries2.add(Entry(i.toFloat(), dataArr2[i]))
        }

        val lineDataSet1 = LineDataSet(entries1, "Company 1")
        lineDataSet1.color = Color.RED
        lineDataSet1.setAxisDependency(YAxis.AxisDependency.LEFT)

        val lineDataSet2 = LineDataSet(entries2, "Company 2")
        lineDataSet2.color = Color.BLUE
        lineDataSet2.setAxisDependency(YAxis.AxisDependency.LEFT)

        val datasets = ArrayList<ILineDataSet>()
        datasets.add(lineDataSet1)
        datasets.add(lineDataSet2)

        LineChart1.data = LineData(datasets)
        LineChart1.invalidate()
    }

    fun initLineChart(){
        val xAxis_ = LineChart1.xAxis
        xAxis_.setDrawLabels(false)
        xAxis_.position = XAxis.XAxisPosition.BOTTOM
        xAxis_.granularity = 1f

        val yAxis_ = LineChart1.axisLeft
        yAxis_.setDrawLabels(false)
    }
}