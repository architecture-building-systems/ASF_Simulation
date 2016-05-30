%Solar generation calculation
%Prageeth Jayathissa
%21.01.2015
clc
%First run combination_analysis_PJ_total.m and overall_minimization.m

eff=[1,0.8,0.7,0.8,0.9,0.8,0.7,0.8,0.7,0.8,0.9,0.8,0.9,1,0.9,0.7,0.9,0.8,0.7,0.8,0.7,0.8,0.9,0.8,0.7,0.,0.7]

eff=eff-0.3


% for ii=1:27
%     X(ii)=sum(I==ii)*eff(ii)
% end
% 

X=0
Y=0

for jj=1:365;
    for kk=1:24;
         if kk>7 & kk<18
             if Index_with_minimal_value(24*(jj-1)+kk,combination_with_minimal_value(24*(jj-1)+kk))==0
                 X=X+1
             else
                X=eff(Index_with_minimal_value(24*(jj-1)+kk,combination_with_minimal_value(24*(jj-1)+kk)))+X
             end
             Y=Y+1
         end
    end
end

solar_eff=X/Y

