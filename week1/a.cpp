//this file is encoded with utf-8
//2020.09.25
//计概实验班第一周作业 算数表达式的计算 实际上建表达式树就是按优先级从低到高建笛卡尔树..那么只需要用单调栈去模拟建立笛卡尔树的过程即可
#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cassert>
#define DB double
using namespace std;
int n,m;
int org[1000009],orp[1000009];
char s[1000009];
double v[1000009];
int ts(char ch)
{
	return ch>='0'&&ch<='9';
}
int isop(char ch)
{
	return ch=='+'||ch=='-'||ch=='*'||ch=='/';
}
int isle(char ch)
{
	return ts(ch)||isop(ch)||ch=='('||ch==')'||ch=='.'||ch==' ';
}
int tm(int id,int op)
{
	int pos=org[op];
	switch(id)
	{
		case 1:printf("格式错误：非法字符'%c'在位置%d",s[op],pos);break;
		case 2:printf("格式错误：括号不匹配！在位置%d",pos);break;
		case 3:printf("格式错误：操作数格式错误！在位置%d",pos);break;
		case 4:printf("格式错误：运算符格式错误！在位置%d",pos);break;
		case 5:printf("数学错误：除以0！在位置%d",pos);break;
		default:printf("????");
	}
	fflush(stdout);
	exit(0);
}
void judge()
{
	static char tpp[1000009];
	memcpy(tpp,s,n+1);
	memset(s,0,n+1);
	int tn=0;
	for(int i=1;i<=n;i++)
		if(tpp[i]!=' ')
			s[++tn]=tpp[i],org[tn]=i;
	n=tn;
	int sm=0;
	if(s[1]=='-')
		s[0]='(';
	for(int i=1;i<=n;i++)
	{
		if(!isle(s[i]))
			tm(1,i);
		if(s[i]=='(')
			sm++;
		else if(s[i]==')')
			sm--;
		if(sm<0)
			tm(2,i);
		if(isop(s[i]))
		{
			if((s[i]!='-'||s[i-1]!='(')&&s[i-1]!=')'&&!ts(s[i-1]))
				tm(4,i);
			if(s[i+1]!='('&&!ts(s[i+1]))
				tm(4,i);
		}
	}
	if(sm!=0)
		tm(2,n);
}
void init()
{
	int fg=0;
	DB cv=0,ps=1;
	if(s[1]=='-')
		v[++m]=0;
	for(int i=1;i<=n;i++)
	{
		if(s[i]==' ')
			continue;
		if(ts(s[i]))
		{
			if(fg)
				cv+=(s[i]-'0')*(ps/=10);
			else
				cv=cv*10+(s[i]-'0');
			if(!ts(s[i+1])&&s[i+1]!='.')
				fg=0,ps=1,v[++m]=cv,cv=0;
			if(s[i+1]=='(')
				v[++m]=-'*';
		}
		else if(s[i]=='.')
		{
			if(fg||!ts(s[i-1])||!ts(s[i+1]))
				tm(3,i);
			fg=1;
		}
		else
		{
			v[++m]=-s[i];
			orp[m]=i;
			if(s[i]=='('&&s[i+1]=='-')
				v[++m]=0;
			if(s[i]==')'&&(ts(s[i+1])||s[i+1]=='('))
				v[++m]=-'*';
		}
	}
}
DB cal(DB a,DB b,char op,int ps)
{
	switch(op)
	{
		case '+':return a+b;
		case '-':return a-b;
		case '*':return a*b;
		case '/':if(b==0)tm(5,ps);return a/b;
	}
}
void solve()
{
	static DB st1[1000009];
	static int st2[1000009];
	static int st3[1000009];
	int tp1=0,tp2=0;
	for(int i=m;i>=1;i--)
		if(v[i]>=0)
			st1[++tp1]=v[i];
		else
		{
			char t=-v[i];
			if(t=='*'||t=='/'||t==')')
				st2[++tp2]=t,st3[tp2]=orp[i];
			else if(t=='+'||t=='-')
			{
				while(st2[tp2]=='*'||st2[tp2]=='/')
				{
					DB nv=cal(st1[tp1],st1[tp1-1],st2[tp2],st3[tp2]);
					tp2--;
					st1[--tp1]=nv;
				}
				st2[++tp2]=t,st3[tp2]=orp[i];
			}
			else if(t=='(')
			{
				while(st2[tp2]!=')')
				{
					DB nv=cal(st1[tp1],st1[tp1-1],st2[tp2],st3[tp2]);
					tp2--;
					st1[--tp1]=nv;
				}
				tp2--;
			}
		}
	while(tp2)
	{
		DB nv=cal(st1[tp1],st1[tp1-1],st2[tp2],st3[tp2]);
		tp2--;
		st1[--tp1]=nv;
	}
	printf("%.2lf",st1[tp1]);
}
int main()
{
	gets(s+1);
	n=strlen(s+1);
	judge();
	init();
	solve();
	return 0;
}