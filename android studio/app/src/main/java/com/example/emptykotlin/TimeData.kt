package com.example.emptykotlin
import java.time.LocalDate
import java.time.LocalDateTime

enum class State{
    START_, DOZE_, AWAKE_,FINISH_
}
class TimeData (val T:LocalDateTime, val S: State)


