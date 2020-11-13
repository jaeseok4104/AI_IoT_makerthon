package com.example.emptykotlin

import android.annotation.SuppressLint
import android.content.Intent
import android.os.AsyncTask
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.text.Editable
import android.widget.TextView
import androidx.annotation.MainThread
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import org.w3c.dom.Text
import java.io.BufferedReader
import java.io.InputStreamReader
import java.lang.Exception
import java.lang.StringBuilder
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLConnection
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter


class MainActivity : AppCompatActivity() {
    var tv : TextView?= null
    var jArr : String? =null
    @SuppressLint("SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)



//      val data = parse(url)
        tv = MainTxt1
        //MainTxt1.text = "END"
        val defaultURL = "http://218.156.165.207/sleep.php"
        val frontURL = "http://198.168.0."
        val endURL = "/sleep.php"
        var url = defaultURL

        URLtext.text = Editable.Factory.getInstance().newEditable(defaultURL)

//        val url = "http://xogud.iptime.org/sleep.php"
        val gPHP = GettingPHP()
        gPHP.execute(url)

        URLBtn.setOnClickListener{
            val gPHP2 = GettingPHP()
            url = URLtext.text.toString()
            gPHP2.execute(url)
        }
//        tv?.text = jArr
        MainBtn1.setOnClickListener {
            val nextIntent = Intent(this, SubActivity3::class.java)
            nextIntent.putExtra("JSONArr",jArr)
            nextIntent.putExtra("test",1)
            startActivity(nextIntent)
        }


    }


    inner class GettingPHP : AsyncTask<String, Int, String>() {
        init {

        }
        override fun doInBackground(vararg p0: String?): String {
            val jsonHtml = StringBuilder()

            try {
                val jsonUrl = URL(p0[0])
                val conn : HttpURLConnection? = jsonUrl.openConnection() as HttpURLConnection

                if(conn!=null) {

                    conn.setConnectTimeout(5000)
                    conn.setReadTimeout(5000)
                    conn.useCaches = false

                    val br = BufferedReader(InputStreamReader(conn.getInputStream(), "UTF-8"))
                        while ( true){
                            val line = br.readLine()
                            if(line == null) break
                            jsonHtml.append(line + "\n")
                        }
                    br.close()
                }
                conn?.disconnect()
            } catch (e:Exception){
                e.printStackTrace();
            }
            return jsonHtml.toString()
        }

        @RequiresApi(Build.VERSION_CODES.O)
        override fun onPostExecute(result: String?) {
            try{
                val test = JSONArray(result)
                jArr = result
//                val T = LocalDateTime.parse(jObj.get("LastUpdate").toString(), DateTimeFormatter.ISO_LOCAL_DATE_TIME)
                //jObj.get("TextData").toString()
                tv?.text = "Success"

            }catch (e:Exception){
                tv?.text = e.toString()
            }
        }
    }

}
