# AI심부름 로봇 (팀 프로젝트 - 4명)
    * 마커 인식        - ros2_aruco / aruco_node.py                  https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco
    * 마커 앞으로 이동 - Project3_turtlebot3 / pub_tb3_pose2d.py  
    * 이미지 토픽변경  - Project3_turtlebot3 / img_compressed2raw  
    * 마커 번호        - Project3_turtlebot3 / track_marker5.py  
    * 목표지점 네비게이션 - Project3_turtlebot3 / bluetooth_waypoint.py  
    * APP에서 송신하는 데이터를 bluetooth_waypoint로 보내기 - Project3_turtlebot3 / pub_goal_msg.py  


---
#### 프로젝트 기간
- 2022.(11.14 ~ 11.30)
---
#### 주 역할
- 소스코드 해석 및 내용 전달  
- 자료조사  
- 테스트 코드 작성  

#### 공통 역할
*(turtlebot3 튜토리얼기반)*  
- SLAM / Navigation 알고리즘을 활용하여 map 제작 및 자율주행 제어  
- AR 마커 인식 프로그래밍  

#### 기술 스택
- Python
- Linux( Ubuntu 20.04 / ROS2 / Raspberry Pi OS) / Arduino IDE  

#### 구현기술
- Publisher, Subscriber로 topic을 발행시켜 여러 노드 간 값 전달
- Action을 활용하여 데이터값 전달
- SLAM 기능을 이용하여 지도 그리기
- Navigation 기능을 통한 자율주행
- Serial 통신을 활용한 Griper 제어
- 블루투스 모듈을 사용하여 로봇제어

---
<table>
  <tr>
    <th>
      [구성도]
    </th>
    <th>
      [구현모습]
    </th>
  </tr> 
  <tr>
    <td>
      <img src="https://user-images.githubusercontent.com/77370836/224692546-ce31f34f-9563-4815-b7b1-38ea10c3dade.png" width="550" height="300">
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/77370836/224692660-e935e5fe-21e5-4f27-a68a-4d9d803c0c78.png" width="550" height="300">
    </td>
  </tr>
  <tr>
    <th colspan="2">
      [프로젝트 영상]
    </th>
  </tr>
  <tr>
    <td colspan="2" align=center> 

https://user-images.githubusercontent.com/77370836/224762941-9f9a2f34-48c1-4e9d-90e0-159f99642a4b.mp4

 </td>
  </tr>
</table>
