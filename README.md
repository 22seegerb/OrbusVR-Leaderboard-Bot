# OrbusVR-Leaderboard-Bot
A Discord Bot for the OrbusVR Cindy Leaderboard at https://leaderboard-orbus.xyz/

Commands:
/top [type = "skill" / "regular"] [playerclass] [amount]
- type: The board to get. By default, it gets the regular board.
- playerclass: The class to filter by. By default, it gets all 8 classes.
- amount: The number of players to get. It can be anywhere from the top 1-15.
<img width="332" alt="top" src="https://user-images.githubusercontent.com/43051577/200961968-19408559-e406-44f1-8936-438830771259.PNG">


/rel_top [player] [type = "skill" / "regular"] [playerclass] [amount]
- player: The player to get the data from.
   -  IMPORTANT: Replace non-ascii values with __
- type: The board to get. By default, it gets the regular board.
- playerclass: The class to filter by. By default, it gets all 8 classes.
- amount: The number of players to get. It can be anywhere from the top 1-15.
<img width="339" alt="reltop" src="https://user-images.githubusercontent.com/43051577/200962025-128784e5-44c0-4845-971b-906c61ec63e7.PNG">


/player [player] [type = "skill" / "regular"] [playerclass] 
- player: The player to get the data from.
   -  IMPORTANT: Replace non-ascii values with __
- type: The board to get. By default, it gets both boards.
- playerclass: The class to filter by. By default, it gets all 8 classes.
<img width="448" alt="player" src="https://user-images.githubusercontent.com/43051577/200962115-92d4ae72-9770-4a69-8ce5-e3a8c6a93bd3.PNG">


/parse [url] [show_relative_position = True / False] [show_graph = True / False]
- url: The URL to get the data from. It must be a valid leaderboard parse link.
- show_relative_position: Show a short comparison of nearby parses, and the position on the leaderboard.
- show_graph: Show the damage graph over time.
Main Parse Command:
<img width="356" alt="parse1" src="https://user-images.githubusercontent.com/43051577/200962143-5e5f968c-5b67-465b-b65d-fd3a6baa7b43.PNG">
Parse Leaderboard Position:
<img width="298" alt="parserel" src="https://user-images.githubusercontent.com/43051577/200962150-02ff855a-2041-422c-8718-cd8b0e58be15.PNG">
