import mysql.connector
from datetime import timedelta, date
import constants
from bs4 import BeautifulSoup, Comment
import urllib2
import requests

blockIdx = 0
pointsIdx = 1
stealsIdx = 2
assistsIdx = 3
turnoversIdx = 4
totalRIdx = 5
tripleDoubleIdx = 6
doubleDoubleIdx = 7
threePMIdx = 8
threePAIdx = 9
offensiveReboundsIdx = 10
defensiveReboundsIdx = 11
minutesPlayedIdx = 12
fieldGoalsIdx = 13
fieldGoalsAttemptedIdx = 14
FTIdx = 15
FTAIdx = 16
usageIdx = 17
ortIdx = 18
drtIdx = 19
tStIdx = 20
eFGIdx = 21


def team_vs_defense_extrapolation(cursor):
    # team vs. position

    # ball handlers
    # PG, SG

    # wings
    # SG, SF

    # bigs
    # SF, PF

    # centers
    # C

    '''
    for ball_handlers
    avg pts, rebounds, offensive stats defensive stats etc....
    for every player that has played vs that team before or on that date

    for all teams:
        get all players who played pg, sg, sf vs that team
            average their performances noe

    '''

    # get all teams
    getBbreffs = "SELECT bbreff FROM team_reference"
    cursor.execute(getBbreffs)

    teams = []

    sqlResults = cursor.fetchall()
    for row in sqlResults:
        teams.append(row[0])

    dateCutOff = constants.teamVsDefenseExtrapolationDateCutOff

    getDates = "SELECT iddates FROM new_dates WHERE iddates >= %s"
    getDatesD = (dateCutOff, )
    cursor.execute(getDates, getDatesD)

    dates = []

    sqlResults = cursor.fetchall()
    for row in sqlResults:
        dates.append(row[0])

    # iterate through all teams and all dates
    getPlayersVsOpponents = "SELECT blocks, points, steals, assists, turnovers, totalRebounds, tripleDouble, doubleDouble, 3PM, 3PA, offensiveRebounds, defensiveRebounds, minutesPlayed, fieldGoals, fieldGoalsAttempted, FT, FTA, usagePercent, offensiveRating, defensiveRating, trueShootingPercent, effectiveFieldGoalPercent FROM performance WHERE opponent = %s AND dateID > 850 AND dateID < %s AND fanduelPosition = %s"
    insertTeamVsDefenseBallHandlers = "INSERT INTO team_vs_ball_handlers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insertTeamVsDefenseWings = "INSERT INTO team_vs_wings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insertTeamVsDefenseBigs = "INSERT INTO team_vs_bigs VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insertTeamVsDefenseCenters = "INSERT INTO team_vs_centers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    tableID = 1
    for team in teams:
        for date in dates:
            # get all players who played vs that team before that day
            # separate players into the buckets aboved based on their position

            # get all ball handlers
            playerVsOpponentsData = (team, date, 'PG')
            cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
            pointGuards = cursor.fetchall()

            playerVsOpponentsData = (team, date, 'SG')
            cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
            shootingGuards = cursor.fetchall()

            playerVsOpponentsData = (team, date, 'SF')
            cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
            smallForwards = cursor.fetchall()

            playerVsOpponentsData = (team, date, 'PF')
            cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
            powerForward = cursor.fetchall()

            # get centers
            playerVsOpponentsData = (team, date, 'C')
            cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
            centers = cursor.fetchall()

            ballHandlers = pointGuards + shootingGuards
            wings = shootingGuards + smallForwards
            bigs = powerForward + smallForwards

            players = {'ball_handlers': ballHandlers, 'wings': wings, 'bigs': bigs, 'centers': centers}
            for key, value in players.items():
                ##############################
                # for each player in bucket
                # (sum all stats / games played till that point)
                blocks = 0
                points = 0
                steals = 0
                assists = 0
                turnovers = 0
                totalRebounds = 0
                tripleDouble = 0
                doubleDouble = 0
                threePM = 0
                threePA = 0
                offensiveRebounds = 0
                defensiveRebounds = 0
                minutesPlayed = 0
                fieldGoals = 0
                fieldGoalsAttempted = 0
                FT = 0
                FTA = 0
                usagePercent = 0
                offensiveRating = 0
                defensiveRating = 0
                trueShootingPercent = 0
                effectiveFieldGoalPercent = 0

                # unlazy but position = ballHandler
                for ballHandler in value:
                    blocks = blocks + ballHandler[blockIdx]
                    points = points + ballHandler[pointsIdx]
                    steals = steals + ballHandler[stealsIdx]
                    assists = assists + ballHandler[assistsIdx]
                    turnovers = turnovers + ballHandler[turnoversIdx]
                    totalRebounds = totalRebounds + ballHandler[totalRIdx]
                    tripleDouble = tripleDouble + ballHandler[tripleDoubleIdx]
                    doubleDouble = doubleDouble + ballHandler[doubleDoubleIdx]
                    threePM = threePM + ballHandler[threePMIdx]
                    threePA = threePA + ballHandler[threePAIdx]
                    offensiveRebounds = offensiveRebounds + ballHandler[offensiveReboundsIdx]
                    defensiveRebounds = defensiveRebounds + ballHandler[defensiveReboundsIdx]
                    minutesPlayed = minutesPlayed + ballHandler[minutesPlayedIdx]
                    fieldGoals = fieldGoals + ballHandler[fieldGoalsIdx]
                    fieldGoalsAttempted = fieldGoalsAttempted + ballHandler[fieldGoalsAttemptedIdx]
                    FT = FT + ballHandler[FTIdx]
                    FTA = FTA + ballHandler[FTAIdx]
                    usagePercent = usagePercent + ballHandler[usageIdx]
                    offensiveRating = offensiveRating + ballHandler[ortIdx]
                    defensiveRating = defensiveRating + ballHandler[drtIdx]
                    trueShootingPercent = trueShootingPercent + ballHandler[tStIdx]
                    effectiveFieldGoalPercent = effectiveFieldGoalPercent + ballHandler[eFGIdx]

                blocksPerMinute = float(blocks) / minutesPlayed if minutesPlayed else 0
                pointsPerMinute = float(points) / minutesPlayed if minutesPlayed else 0
                stealsPerMinute = float(steals) / minutesPlayed if minutesPlayed else 0
                assistsPerMinute = float(assists) / minutesPlayed if minutesPlayed else 0
                turnoversPerMinute = float(turnovers) / minutesPlayed if minutesPlayed else 0
                tripleDoubles = float(tripleDouble) / len(ballHandlers) if len(ballHandlers) else 0
                doubleDoubles = float(doubleDouble) / len(ballHandlers) if len(ballHandlers) else 0
                threePP = float(threePM) / float(threePA) if threePA else 0
                offensiveReboundsPerMinute = float(offensiveRebounds) / minutesPlayed if minutesPlayed else 0
                defensiveReoundsPerMinute = float(defensiveRebounds) / minutesPlayed if minutesPlayed else 0
                fieldGoalP = float(fieldGoals) / float(fieldGoalsAttempted) if fieldGoalsAttempted else 0
                FTP = float(FT) / float(FTA) if FTA else 0
                usagePercentTot = usagePercent / len(ballHandlers) if len(ballHandlers) else 0
                offensiveRatingTot = offensiveRating / len(ballHandlers) if len(ballHandlers) else 0
                defensiveRatingTot = defensiveRating / len(ballHandlers) if len(ballHandlers) else 0
                trueShooting = points / (2 * (float(fieldGoalsAttempted) + 0.44 * FTA)) if fieldGoalsAttempted else 0
                effectiveFieldGoal = (float(fieldGoals) + 0.5 * float(threePM)) / float(
                    fieldGoalsAttempted) if fieldGoalsAttempted else 0

                # get team id
                teamIDQ = "SELECT teamID FROM team_reference WHERE bbreff = %s"
                teamIDD = (team,)
                cursor.execute(teamIDQ, teamIDD)

                teamID = 0
                for id in cursor.fetchall():
                    teamID = id[0]

                teamVsPlayerData = (tableID, teamID, date, blocks, points, steals, assists, turnovers, totalRebounds,
                                    tripleDouble, doubleDouble,
                                    threePM, threePA, offensiveRebounds, defensiveRebounds, minutesPlayed, fieldGoals,
                                    fieldGoalsAttempted, FT, FTA, blocksPerMinute, pointsPerMinute, stealsPerMinute,
                                    assistsPerMinute, turnoversPerMinute, tripleDoubles, doubleDoubles, threePP,
                                    offensiveReboundsPerMinute, defensiveReoundsPerMinute, fieldGoalP, FTP,
                                    usagePercentTot,
                                    offensiveRatingTot, defensiveRatingTot, trueShooting, effectiveFieldGoal)

                if key == 'ball_handlers':
                    cursor.execute(insertTeamVsDefenseBallHandlers, teamVsPlayerData)
                if key == 'wings':
                    cursor.execute(insertTeamVsDefenseWings, teamVsPlayerData)
                if key == 'bigs':
                    cursor.execute(insertTeamVsDefenseBigs, teamVsPlayerData)
                if key == 'centers':
                    cursor.execute(insertTeamVsDefenseCenters, teamVsPlayerData)

                cnx.commit()
                tableID = tableID + 1


if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.databaseUser,
                                  host=constants.databaseHost,
                                  database=constants.databaseName,
                                  password=constants.databasePassword)
    cursor = cnx.cursor(buffered=True)

    team_vs_defense_extrapolation(cursor)

    cursor.close()
    cnx.commit()
    cnx.close()