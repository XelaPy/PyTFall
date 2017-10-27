init -5 python:
    class BrothelBlock(PrivateBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 30, "Glass": 5}
        COST = 10000
        ID = "Brothel"
        IMG = "content/buildings/upgrades/room.jpg"
        def __init__(self, name="Brothel", instance=None, desc="Rooms to freck in!",
                     img="content/buildings/upgrades/room.jpg", build_effort=0, materials=None,
                     in_slots=2, cost=500, **kwargs):
            super(BrothelBlock, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.capacity = in_slots
            self.type = "personal_service"
            self.jobs = set([simple_jobs["Whore Job"]])
            self.workable = True

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 5 # Same
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.

        def has_workers(self):
            # Check if the building still has someone availbile to do the job.
            # We just check this for
            return list(i for i in self.instance.available_workers if self.all_occs & i.occupations)

        def business_control(self):
            while 1:
                yield self.env.timeout(self.time)

                if self.res.count == 0 and not self.has_workers():
                    break

            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no workers available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            self.instance.nd_ups.remove(self)

        def request_room(self, client, worker):
            """Requests a room from Sim'Py, under the current code, this will not be called if there are no rooms available...
            """
            with self.res.request() as request:
                yield request

                # All is well and the client enters:
                temp = "{}: {} and {} enter the room.".format(self.env.now, client.name, worker.name)
                self.log(temp)

                # This line will make sure code halts here until run_job ran it's course...
                yield self.env.process(self.run_job(client, worker))

                # Action (Job) ran it's course and client is leaving...
                temp = "{}: {} leaves the {}.".format(self.env.now, client.name, self.name)
                self.log(temp)
                # client.flag("jobs_busy").interrupt()
            client.del_flag("jobs_busy")

        def run_job(self, client, worker):
            """Waits for self.time delay and calls the job...
            """
            yield self.env.timeout(self.time)
            if config.debug:
                temp = "{}: Debug: {} Building Resource in use!".format(self.env.now, set_font_color(self.res.count, "red"))
                self.log(temp)

            temp = "{}: {} and {} did their thing!".format(self.env.now, set_font_color(worker.name, "pink"), client.name)
            self.log(temp)

            # Visit counter:
            client.up_counter("got_serviced_by" + worker.id)
            # Execute the job:
            job, building = self.job, self.instance
            log = NDEvent(job=job, char=worker, loc=building, business=self)
            worker.jobpoints -= 100
            job.settle_workers_disposition(worker, log)

            difficulty = building.tier
            effectiveness = job.effectiveness(worker, difficulty, log)

            # job.payout_mod() # TODO
            job.acts(worker=worker, client=client, building=building, log=log, effectiveness=effectiveness)
            log.after_job()
            NextDayEvents.append(log)

            # We return the char to the nd list:
            self.instance.available_workers.insert(0, worker)
