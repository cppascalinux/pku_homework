//written by cdc

#include <cstdio>
#include <algorithm>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

#define MAX_SIZE 220000000
#define MIN_FREQ 3
#define MAX_VOCAB_NUM 2000
#define WINDOW_WIDTH 4

char alltext[MAX_SIZE];
char* token[MAX_SIZE];

unordered_map<string, int> word_freq_map;
vector< pair<string, int> > word_freq;

unordered_map<string, int> word2idx;
vector<string> idx2word;

int A[MAX_VOCAB_NUM][MAX_VOCAB_NUM];

int main()
{
	freopen("2004_ansi.txt", "r", stdin);
	
	char *ptr = alltext;
	int num_tokens = 0;
	while (scanf("%s", ptr) != EOF)
	{
		int len = strlen(ptr);
		token[num_tokens++] = ptr;
		
		char *pos = strrchr(ptr, '/');
		if (*(pos+1) == 'n' || *(pos+1) == 'v') //noun or verb
			++ word_freq_map[string(ptr)];
			
		ptr += len + 1;
	}
	
	word_freq.insert(word_freq.begin(), word_freq_map.begin(), word_freq_map.end());
	sort(word_freq.begin(), word_freq.end(), 
			[](const pair<string, int>&a, const pair<string, int>&b) -> bool
			{return a.second > b.second;}
		);
	
	int N = min((int)word_freq.size(), MAX_VOCAB_NUM);
	for (int i = 0; i < N; ++ i)
	{
		word2idx[word_freq[i].first] = i;
		idx2word.push_back(word_freq[i].first);
	}
	
	for (int i = 0; i < num_tokens; ++ i)
	{
		char *now = token[i];
		auto tmp = word2idx.find(string(now));
		if (tmp == word2idx.end()) continue;
		int now_idx = tmp->second;
		
		for (int j = i-1; j >= 0 && j>=i-WINDOW_WIDTH; --j)
		{
			char *last = token[j];
			
			auto tmp = word2idx.find(string(last));
			if (tmp == word2idx.end()) continue;
			int last_idx = tmp->second;
			
			++ A[last_idx][now_idx];
			++ A[now_idx][last_idx];
		}
	}
	
	freopen("noun+verb.txt", "w", stdout);
	for (int i = 0; i < N; ++ i) 
		printf("%d %s\n", i, idx2word[i].c_str());
	
	freopen("noun+verb_graph.txt", "w", stdout);
	for (int i = 0; i < N; ++ i, printf("\n"))
		for (int j = 0; j < N; ++ j)
			printf("%d ", A[i][j]);
			
	return 0;
}
