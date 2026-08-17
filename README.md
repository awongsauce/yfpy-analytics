## YFPY-analytics - YFPY fork

Dumbing down the API for simpletons (me)

Credit to *Author: Wren J. R. (uberfastman)*

<sup>Detailed documentation on original YFPY can be found at [https://yfpy.uberfastman.com](https://yfpy.uberfastman.com).</sup>

### Usage

* **Getting draft results**
```
df = analytics.expanded_draft_results(query)
```
```python
df
```


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

<br/>

* **Viewing Average Draft Position (ranking) vs actual**

```
df_draft_adp = analytics.league_draft_vs_ADP(df)
```
<img width="1000" height="600" alt="test_adp_3" src="https://github.com/user-attachments/assets/d73e4e89-15e0-4a2c-b7c3-ea3fad8bed53" />


<br/>

 * **Visualizing how close h2h matchups are**

```
current_week = 20

league_matchups = query.get_league_matchups_by_week(current_week)
df = pd.DataFrame(league_matchups)
week_results = analytics.week_results_concat_explode(df)
analytics.h2h_charts(week_results)
```
<img width="2573" height="1637" alt="Muh Queen of the 7 Parishes vs Luka Dongitch" src="https://github.com/user-attachments/assets/d13a42dc-919e-40ff-a45e-4e98e55c1acb" />



<br/>

* **Visualizing how each team performed by percentile compared to top team in each category**

```
analytics.normalized_performance_chart(week_results)
```
<img width="1400" height="700" alt="Team performance" src="https://github.com/user-attachments/assets/35802bf5-3af5-4092-8b8c-5510ab32ed9e" />



<br/>

* **Visualizing team performance in heat chart of simple ranking (higher number = better)**

```
analytics.cat_heat_map_chart(week_results)
```
<img width="2816" height="1578" alt="Cat_heat_map" src="https://github.com/user-attachments/assets/0c416aa9-5b68-4085-b776-7a699ea9f772" />


<br/>

* **Seeing cumulative performance over the whole season**

```
full_season_df = full_season_standings(18)
season_standings_chart(full_season_df)

```
<img width="4395" height="1918" alt="Season_long" src="https://github.com/user-attachments/assets/e3c7d118-a546-430b-b9c4-29b2a1530f28" />




<br/>

* **Getting league transaction history**

```
df = analytics.get_transactions(query)
df2 = analytics.insert_transact_info(df)
```
```
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
* 












