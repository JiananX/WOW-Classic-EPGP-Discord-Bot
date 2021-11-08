def basic_report_query(code):
    return '''
            {
              reportData {
                report(code: "%s") {
                  masterData {
                    actors(type: "Player") {
                      id
                      name
                      subType
                    }
                  }
                  fights(killType: Kills){
                    id,
                    name,
                    startTime,
                    endTime,
                    friendlyPlayers
                  }
                }
              }
            }
            ''' % (code)


def event_query(code, fight, spell_id):
    return '''
            {
              reportData {
                report(code: "%s") {
                  events(fightIDs: [%s], startTime: %s, endTime: %s, abilityID: %s, dataType: Casts){
                    data
                  }
                }
              }
            }
            ''' % (code, fight.ID, fight.STARTTIME, fight.ENDTIME, spell_id)


def death_query(code, fight):
    return '''
            {
              reportData {
                report(code: "%s") {
                  events(fightIDs: [%s], startTime: %s, endTime: %s,dataType: Deaths){
                    data
                  }
                }
              }
            }
            ''' % (code, fight.ID, fight.STARTTIME, fight.ENDTIME)
