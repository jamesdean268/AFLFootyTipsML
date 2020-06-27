SELECT 
    TEAM_STATS_PER_ROUND.*, 
    TEAM_DATA.score, 
    TEAM_DATA.home_away
    FROM
    (
        SELECT
        PLAYER_STATS_PER_ROUND.team, 
        PLAYER_STATS_PER_ROUND.year, 
        PLAYER_STATS_PER_ROUND.round, 
        Sum(PLAYER_STATS_PER_ROUND.DI_Avg) AS SumOfDI_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.KI_Avg) AS SumOfKI_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.MK_Avg) AS SumOfMK_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.HB_Avg) AS SumOfHB_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.GL_Avg) AS SumOfGL_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.BH_Avg) AS SumOfBH_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.HO_Avg) AS SumOfHO_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.TK_Avg) AS SumOfTK_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.RB_Avg) AS SumOfRB_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.I5_Avg) AS SumOfI5_Avg, 
        Sum(PLAYER_STATS_PER_ROUND.CL_Avg) AS SumOfCL_Avg
        FROM
        (
            SELECT GAMES_PLAYED.*, 
            PLAYER_STATS.games_played, 
            PLAYER_STATS.DI_Avg, 
            PLAYER_STATS.KI_Avg, 
            PLAYER_STATS.MK_Avg, 
            PLAYER_STATS.HB_Avg, 
            PLAYER_STATS.GL_Avg, 
            PLAYER_STATS.BH_Avg, 
            PLAYER_STATS.HO_Avg, 
            PLAYER_STATS.TK_Avg, 
            PLAYER_STATS.RB_Avg, 
            PLAYER_STATS.I5_Avg, 
            PLAYER_STATS.CL_Avg
            FROM GAMES_PLAYED INNER JOIN PLAYER_STATS 
            ON 
            (GAMES_PLAYED.team = PLAYER_STATS.team) AND 
            (GAMES_PLAYED.year = PLAYER_STATS.year) AND 
            (GAMES_PLAYED.player = PLAYER_STATS.player)
        ) AS PLAYER_STATS_PER_ROUND
        GROUP BY 
        PLAYER_STATS_PER_ROUND.team, 
        PLAYER_STATS_PER_ROUND.year, 
        PLAYER_STATS_PER_ROUND.round
    ) AS TEAM_STATS_PER_ROUND
    INNER JOIN TEAM_DATA 
    ON 
    (TEAM_STATS_PER_ROUND.round = TEAM_DATA.round) AND 
    (TEAM_STATS_PER_ROUND.year = TEAM_DATA.year) AND 
    (TEAM_STATS_PER_ROUND.team = TEAM_DATA.team)
;