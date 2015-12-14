sol=zeros(8760,2);

for i=1:8760
    if END(i,1)==1
        sol(i,1)=-75;
    elseif END(i,1)==2
        sol(i,1)=-60;
    elseif END(i,1)==3
        sol(i,1)=-45;
    elseif END(i,1)==4
        sol(i,1)=-30;
    elseif END(i,1)==5
        sol(i,1)=-15;
    elseif END(i,1)==6
        sol(i,1)=0;
    elseif END(i,1)==7
        sol(i,1)=15;
    elseif END(i,1)==8
        sol(i,1)=30;
    elseif END(i,1)==9
        sol(i,1)=45;
    elseif END(i,1)==10
        sol(i,1)=60;
    elseif END(i,1)==11
        sol(i,1)=75;
    elseif END(i,1)==12
        sol(i,1)=90;
    end
    
    if END(i,2)==1
        sol(i,2)=111;
    elseif END(i,2)==2
        sol(i,2)=112;
    elseif END(i,2)==3
        sol(i,2)=113;
    elseif END(i,2)==4
        sol(i,2)=121;
    elseif END(i,2)==5
        sol(i,2)=122;
    elseif END(i,2)==6
        sol(i,2)=123;
    elseif END(i,2)==7
        sol(i,2)=131;
    elseif END(i,2)==8
        sol(i,2)=132;
    elseif END(i,2)==9
        sol(i,2)=133;
    elseif END(i,2)==10
        sol(i,2)=211;
    elseif END(i,2)==11
        sol(i,2)=212;
    elseif END(i,2)==12
        sol(i,2)=213;
    elseif END(i,2)==13
        sol(i,2)=221;
    elseif END(i,2)==14
        sol(i,2)=222;
    elseif END(i,2)==15
        sol(i,2)=223;
    elseif END(i,2)==16
        sol(i,2)=231;
    elseif END(i,2)==17
        sol(i,2)=232;
    elseif END(i,2)==18
        sol(i,2)=233;
    elseif END(i,2)==19
        sol(i,2)=311;
    elseif END(i,2)==20
        sol(i,2)=312;
    elseif END(i,2)==21
        sol(i,2)=313;
    elseif END(i,2)==22
        sol(i,2)=321;
    elseif END(i,2)==23
        sol(i,2)=322;
    elseif END(i,2)==24
        sol(i,2)=323;
    elseif END(i,2)==25
        sol(i,2)=331;
    elseif END(i,2)==26
        sol(i,2)=332;
    elseif END(i,2)==27
        sol(i,2)=333;
    end
end