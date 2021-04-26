# Moguding
MoGuDing check in/out automatically

### Usage:   
1. Setup encrypted secrets in github workflow: [link](https://docs.github.com/cn/actions/reference/encrypted-secrets)  
2. Deploy github action workflow.  
3. Modify your serverchan skey  
> ![image](https://user-images.githubusercontent.com/30458572/116025058-2b755080-a682-11eb-9633-1d7d88fe09f9.png)
5. Enjoy it :)  
![image](https://user-images.githubusercontent.com/30458572/115913879-c532d700-a4a3-11eb-9f4c-8b4a82aef996.png)

### Screenshots:
1. Sign-in & sign-out  
![image](https://user-images.githubusercontent.com/30458572/115913491-3faf2700-a4a3-11eb-82be-d284cdf114bd.png)

2. Write weekly report
> 2-1. Prepared weekly-report content(Remeber, need to clear line break in content), I call it [weeklyReport.json]  
> ![image](https://user-images.githubusercontent.com/30458572/116024456-d08f2980-a680-11eb-8612-60574c205bce.png)

> 2-2. Execute it [python3 Main.py -week -file weeklyReport.json]  
> ![image](https://user-images.githubusercontent.com/30458572/116024755-780c5c00-a681-11eb-917d-06dfb508e362.png)

> 2-3. Got a feedback in ServerChan.  
> ![image](https://user-images.githubusercontent.com/30458572/116024853-b73aad00-a681-11eb-836b-893392866ba7.png)
