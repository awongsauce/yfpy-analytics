```python
df = analytics.expanded_draft_results(query)
```

    2026-05-20 03:36:47.029 - ERROR - query.py - yfpy.query:544 - No data found when attempting extraction from fields: ['league', 'players']
    


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Overall pick</th>
      <th>Round</th>
      <th>team_id</th>
      <th>player_id</th>
      <th>full_name</th>
      <th>Team code</th>
      <th>Team</th>
      <th>player_name_clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>466.l.87564.t.4</td>
      <td>466.p.5352</td>
      <td>Nikola Jokić</td>
      <td>DEN</td>
      <td>LeGolf Injury</td>
      <td>Nikola Jokic</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>466.l.87564.t.10</td>
      <td>466.p.10094</td>
      <td>Victor Wembanyama</td>
      <td>SAS</td>
      <td>Knecht 4</td>
      <td>Victor Wembanyama</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>466.l.87564.t.2</td>
      <td>466.p.5185</td>
      <td>Giannis Antetokounmpo</td>
      <td>MIL</td>
      <td>Paolamelo &amp; The Uncs</td>
      <td>Giannis Antetokounmpo</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>466.l.87564.t.9</td>
      <td>466.p.6022</td>
      <td>Shai Gilgeous-Alexander</td>
      <td>OKC</td>
      <td>One Injury After Another</td>
      <td>Shai Gilgeous-Alexander</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>1</td>
      <td>466.l.87564.t.12</td>
      <td>466.p.6014</td>
      <td>Luka Dončić</td>
      <td>LAL</td>
      <td>Bronny's Bookie</td>
      <td>Luka Doncic</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>151</th>
      <td>152</td>
      <td>13</td>
      <td>466.l.87564.t.1</td>
      <td>466.p.6567</td>
      <td>Quentin Grimes</td>
      <td>PHI</td>
      <td>Muh Queen of the 7 Parishes</td>
      <td>Quentin Grimes</td>
    </tr>
    <tr>
      <th>152</th>
      <td>153</td>
      <td>13</td>
      <td>466.l.87564.t.3</td>
      <td>466.p.5764</td>
      <td>Lonzo Ball</td>
      <td>CLE</td>
      <td>The Book Of Joel</td>
      <td>Lonzo Ball</td>
    </tr>
    <tr>
      <th>153</th>
      <td>154</td>
      <td>13</td>
      <td>466.l.87564.t.8</td>
      <td>466.p.4892</td>
      <td>Klay Thompson</td>
      <td>DAL</td>
      <td>Luka Dongitch</td>
      <td>Klay Thompson</td>
    </tr>
    <tr>
      <th>154</th>
      <td>155</td>
      <td>13</td>
      <td>466.l.87564.t.6</td>
      <td>466.p.6580</td>
      <td>Ayo Dosunmu</td>
      <td>MIN</td>
      <td>Davis BerTrans Rights</td>
      <td>Ayo Dosunmu</td>
    </tr>
    <tr>
      <th>155</th>
      <td>156</td>
      <td>13</td>
      <td>466.l.87564.t.5</td>
      <td>466.p.10282</td>
      <td>Isaiah Collier</td>
      <td>UTA</td>
      <td>Barnes and Noble</td>
      <td>Isaiah Collier</td>
    </tr>
  </tbody>
</table>
<p>156 rows × 8 columns</p>
</div>




```python
df_draft_adp = analytics.league_draft_vs_ADP(df)
```

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:81: FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.
      
    


    
![png](output_5_1.png)
    


    Would you like to save the file? (y/n):  y
    What would you like to name the file?  2026-05-20 test
    


```python
current_week = 20

league_matchups = query.get_league_matchups_by_week(current_week)
df = pd.DataFrame(league_matchups)
week_results = analytics.week_results_concat_explode(df)
```

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:263: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = diff[j]
    


```python
analytics.h2h_charts(week_results)
```

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:333: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = norm_diff[j]
    


    
![png](output_7_1.png)
    


    Save these plots? (y/n):  y
    

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:333: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = norm_diff[j]
    


    
![png](output_7_4.png)
    


    Save these plots? (y/n):  y
    

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:333: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = norm_diff[j]
    


    
![png](output_7_7.png)
    


    Save these plots? (y/n):  y
    

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:333: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = norm_diff[j]
    


    
![png](output_7_10.png)
    


    Save these plots? (y/n):  y
    

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:333: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = norm_diff[j]
    


    
![png](output_7_13.png)
    


    Save these plots? (y/n):  n
    

    Charts not saved
    

    C:\Users\alber\anaconda3\Lib\site-packages\yfpy\analytics.py:333: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
      val = norm_diff[j]
    


    
![png](output_7_17.png)
    


    Save these plots? (y/n):  n
    

    Charts not saved
    


```python
analytics.normalized_performance_chart(week_results)
```


    
![png](output_8_0.png)
    


    Save this chart? (y/n):  y
    What would you like to name the file?  testee
    


```python
analytics.cat_heat_map_chart(week_results)
```


    
![png](output_9_0.png)
    


    Save this chart? (y/n):  y
    What would you like to name the file?  wowee
    


```python
df = analytics.get_transactions(query)
```


```python
df2 = analytics.insert_transact_info(df)
df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>Log</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>Team name</th>
      <th>Team key</th>
      <th>NBA team</th>
      <th>player_1</th>
      <th>destination_team_1</th>
      <th>source_team_1</th>
      <th>player_2</th>
      <th>destination_team_2</th>
      <th>source_team_2</th>
      <th>PST datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>466.l.87564.tr.403</td>
      <td>403</td>
      <td>drop</td>
      <td>successful</td>
      <td>1774188348</td>
      <td>{'player': Player({\n  "display_position": "G,...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>Barnes and Noble</td>
      <td>466.l.87564.t.5</td>
      <td>HOU</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 07:05:48-07:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>466.l.87564.tr.401</td>
      <td>401</td>
      <td>add/drop</td>
      <td>successful</td>
      <td>1774167243</td>
      <td>[{'player': Player({\n  "display_position": "C...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>Barnes and Noble</td>
      <td>466.l.87564.t.5</td>
      <td>PHX</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 01:14:03-07:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>466.l.87564.tr.400</td>
      <td>400</td>
      <td>add/drop</td>
      <td>successful</td>
      <td>1774167243</td>
      <td>[{'player': Player({\n  "display_position": "C...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>LeGolf Injury</td>
      <td>466.l.87564.t.4</td>
      <td>BOS</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 01:14:03-07:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>466.l.87564.tr.399</td>
      <td>399</td>
      <td>drop</td>
      <td>successful</td>
      <td>1774165373</td>
      <td>{'player': Player({\n  "display_position": "G"...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>LeGolf Injury</td>
      <td>466.l.87564.t.4</td>
      <td>OKC</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 00:42:53-07:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>466.l.87564.tr.398</td>
      <td>398</td>
      <td>drop</td>
      <td>successful</td>
      <td>1774131716</td>
      <td>{'player': Player({\n  "display_position": "G"...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>Knecht 4</td>
      <td>466.l.87564.t.10</td>
      <td>MEM</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-21 15:21:56-07:00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>353</th>
      <td>466.l.87564.tr.5</td>
      <td>5</td>
      <td>add</td>
      <td>successful</td>
      <td>1759736734</td>
      <td>{'player': Player({\n  "display_position": "G"...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>Muh Queen of the 7 Parishes</td>
      <td>466.l.87564.t.1</td>
      <td>LAL</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-10-06 00:45:34-07:00</td>
    </tr>
    <tr>
      <th>354</th>
      <td>466.l.87564.tr.4</td>
      <td>4</td>
      <td>add</td>
      <td>successful</td>
      <td>1759736734</td>
      <td>{'player': Player({\n  "display_position": "F"...</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>Luka Dongitch</td>
      <td>466.l.87564.t.8</td>
      <td>ATL</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-10-06 00:45:34-07:00</td>
    </tr>
    <tr>
      <th>355</th>
      <td>466.l.87564.tr.3</td>
      <td>3</td>
      <td>commish</td>
      <td>successful</td>
      <td>1758773695</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-09-24 21:14:55-07:00</td>
    </tr>
    <tr>
      <th>356</th>
      <td>466.l.87564.tr.2</td>
      <td>2</td>
      <td>commish</td>
      <td>successful</td>
      <td>1758668200</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-09-23 15:56:40-07:00</td>
    </tr>
    <tr>
      <th>357</th>
      <td>466.l.87564.tr.1</td>
      <td>1</td>
      <td>commish</td>
      <td>successful</td>
      <td>1758668200</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-09-23 15:56:40-07:00</td>
    </tr>
  </tbody>
</table>
<p>358 rows × 22 columns</p>
</div>




```python
df_t_min = df2.iloc[:,-12:]
df_t_min
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adds</th>
      <th>drops</th>
      <th>Team name</th>
      <th>Team key</th>
      <th>NBA team</th>
      <th>player_1</th>
      <th>destination_team_1</th>
      <th>source_team_1</th>
      <th>player_2</th>
      <th>destination_team_2</th>
      <th>source_team_2</th>
      <th>PST datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td></td>
      <td>Tari Eason</td>
      <td>Barnes and Noble</td>
      <td>466.l.87564.t.5</td>
      <td>HOU</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 07:05:48-07:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Oso Ighodaro</td>
      <td>Cam Spencer</td>
      <td>Barnes and Noble</td>
      <td>466.l.87564.t.5</td>
      <td>PHX</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 01:14:03-07:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mitchell Robinson</td>
      <td>Tristan da Silva</td>
      <td>LeGolf Injury</td>
      <td>466.l.87564.t.4</td>
      <td>BOS</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 01:14:03-07:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td></td>
      <td>Ajay Mitchell</td>
      <td>LeGolf Injury</td>
      <td>466.l.87564.t.4</td>
      <td>OKC</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-22 00:42:53-07:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td></td>
      <td>Ty Jerome</td>
      <td>Knecht 4</td>
      <td>466.l.87564.t.10</td>
      <td>MEM</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2026-03-21 15:21:56-07:00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>353</th>
      <td>Collin Sexton</td>
      <td></td>
      <td>Muh Queen of the 7 Parishes</td>
      <td>466.l.87564.t.1</td>
      <td>LAL</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-10-06 00:45:34-07:00</td>
    </tr>
    <tr>
      <th>354</th>
      <td>Zaccharie Risacher</td>
      <td></td>
      <td>Luka Dongitch</td>
      <td>466.l.87564.t.8</td>
      <td>ATL</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-10-06 00:45:34-07:00</td>
    </tr>
    <tr>
      <th>355</th>
      <td></td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-09-24 21:14:55-07:00</td>
    </tr>
    <tr>
      <th>356</th>
      <td></td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-09-23 15:56:40-07:00</td>
    </tr>
    <tr>
      <th>357</th>
      <td></td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2025-09-23 15:56:40-07:00</td>
    </tr>
  </tbody>
</table>
<p>358 rows × 12 columns</p>
</div>




```python
df2.value_counts("adds").iloc[1:10] # show most added players
```




    adds
    Dylan Harper        6
    Ajay Mitchell       5
    Isaiah Collier      5
    Andre Drummond      5
    Tre Jones           5
    Kyle Kuzma          5
    Ryan Kalkbrenner    4
    Peyton Watson       4
    Kyle Filipowski     4
    Name: count, dtype: int64




```python
df2.value_counts("drops").iloc[1:10] # show most dropped players
```




    drops
    Ajay Mitchell      5
    Andre Drummond     5
    Kyle Kuzma         5
    Isaiah Collier     5
    Dylan Harper       5
    Moses Moody        4
    Tre Jones          4
    Sam Hauser         4
    Kyle Filipowski    4
    Name: count, dtype: int64




```python
df.value_counts("NBA team").iloc[1:10] # show NBA teams with most transactions (adds + drops)
```




    NBA team
    BKN    18
    UTA    18
    IND    18
    DEN    17
    SAS    16
    WAS    16
    OKC    15
    SAC    14
    LAC    14
    Name: count, dtype: int64




```python

```
